//
//  TweetTableViewController.swift
//  Smashtag
//
//  Created by Joe Burg  on 12/7/16.
//  Copyright © 2016 Joe Burg . All rights reserved.
//

import CoreData
import Twitter
import UIKit


class TweetTableViewController: UITableViewController, UITextFieldDelegate {

    
    // MARK: Model
    
    // set this to the database you want to work with
    var managedObjectContext: NSManagedObjectContext? =
        (UIApplication.sharedApplication().delegate as? AppDelegate)?.managedObjectContext
    
    
    // the model is an array of an array of tweets
    // this allows you to keep adding sections 
    // this is a really good technique to use for tables
    var tweets = [Array<Twitter.Tweet>]() {
        didSet {
            tableView.reloadData()
        }
    }
    
    // allow people to search for tweets within the model
    var searchText: String? {
        didSet {
            // first remove the previous tweets
            tweets.removeAll()
            // search for the new tweets
            searchForTweets()
            title = searchText
        }
    }
    
    
    
    
    // MARK: Fetching Tweets
    

    // this uses the Twitter framework that we added to the workspace
    // create a var that does the request
    private var twitterRequest: Twitter.Request? {
        // make sure the query is not nil and not empty
        if let query = searchText where !query.isEmpty {
            // only return 100 tweets max
            return Twitter.Request(search: query + " -filter:retweets", count: 100)
        }
        return nil
    }
    
    
    private var lastTwitterRequest: Twitter.Request?
    
    // now search for the tweets
    private func searchForTweets()
    {
        if let request = twitterRequest {
            lastTwitterRequest = request
            // create a weak pointer to self to you tell it can leave the 
            // heap if the use goes somewhere else while a large process is occuring
            request.fetchTweets { [weak weakSelf = self] newTweets in
                // the closure is executed off the main queue so you need to
                // dispatch async (use trailing closure syntax)
                dispatch_async(dispatch_get_main_queue()) {
                    // if the user leaves before a request is done processing
                    // and then comes back searching for new tweets, then we
                    // dont want the old request to show up
                    if request == weakSelf?.lastTwitterRequest {
                        if !newTweets.isEmpty {
                            // want the new tweets at the beginning of the array
                            // this wont happend if the closure leaves the heap
                            weakSelf?.tweets.insert(newTweets, atIndex: 0)
                            
                            // update the database that stores the users that tweeted
                            weakSelf?.updateDatabase(newTweets)
                        }
                    }
                }
            }
        }
    }
    
    
    // this method takes Twitter tweets and turns them into NSManagedObjects and 
    // puts them in the database
    private func updateDatabase(newTweets: [Twitter.Tweet]) {
        // we need the context to create a hook to the database
        // the block helps with multithreading
        managedObjectContext?.performBlock {
            for twitterInfo in newTweets {
                // create a new, unique tweet with that Twitter info
                // _ = means that you know the method returns something but we dont care what it is
                _ = Tweet.tweetWithTwitterInfo(twitterInfo, inManagedObjectContext: self.managedObjectContext!)
            }
            
            // save to the database
            do {
                try self.managedObjectContext?.save()
            } catch let error {
                print("Core Data Error: \(error)")
            }
        }
        
        // print the database stats 
        printDatabaseStatistics()
        print("done printing database statistics")
    }
    
    
    // this method prints the database stats 
    private func printDatabaseStatistics() {
        // always put managed context object stuff in a block
        managedObjectContext?.performBlock {
            if let results = try? self.managedObjectContext!.executeFetchRequest(NSFetchRequest(entityName: "TwitterUser")) {
                print("\(results.count) TwitterUsers")
            }
            
            // this is a more efficient way to count the objects ...
            let tweetCount = self.managedObjectContext!.countForFetchRequest(NSFetchRequest(entityName: "Tweet"), error: nil)
            print("\(tweetCount) Tweets")
        }
    }
    
    
    // prepare segue between this MVC and the Tweeters MVC
    override func prepareForSegue(segue: UIStoryboardSegue, sender: AnyObject?) {
        if segue.identifier == "TweetersMentioningSearchTerm" {
            if let tweetersTVC = segue.destinationViewController as? TweetersTableViewController {
                tweetersTVC.mention = searchText
                tweetersTVC.managedObjectContext = managedObjectContext
            }
        }
    }
    
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        // set the row's height to automatic dimensions (set estimated too)
        tableView.estimatedRowHeight = tableView.rowHeight
        tableView.rowHeight = UITableViewAutomaticDimension
        
        // set the initial view for the users 
        // searchText = "#stanford"

    }

    // MARK: - UITableViewDataSource

    // these methods should look very simple 
    // the art of keeping them down to one line is well thought out data structures
    override func numberOfSectionsInTableView(tableView: UITableView) -> Int {
        // #warning Incomplete implementation, return the number of sections
        return tweets.count
    }

    override func tableView(tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        // #warning Incomplete implementation, return the number of rows
        return tweets[section].count
    }
    
    
    // make a cell
    // reuse identifier
    private struct Storyboard {
        static let TweetCellIdentifier = "Tweet"
    }

    // this is the heart of a dynamic view table
    override func tableView(tableView: UITableView, cellForRowAtIndexPath indexPath: NSIndexPath) -> UITableViewCell {
        let cell = tableView.dequeueReusableCellWithIdentifier(Storyboard.TweetCellIdentifier, forIndexPath: indexPath)

        // tweets is an array of arrays
        let tweet = tweets[indexPath.section][indexPath.row]
        if let tweetCell = cell as? TweetTableViewCell {
            tweetCell.tweet = tweet
        }

        return cell
    }
    
    
    // search text field in the UI 
    @IBOutlet weak var searchTextField: UITextField!
    {
        didSet {
            searchTextField.delegate = self
            searchTextField.text = searchText
        }
    }
    
    
    // when someone hits return, this sets the searchText and hides the keyboard
    func textFieldShouldReturn(textField: UITextField) -> Bool {
        textField.resignFirstResponder()
        searchText = textField.text
        return true
    }
    

    // these methods are used when you want the user to edit the rows
    
    /*
    // Override to support conditional editing of the table view.
    override func tableView(tableView: UITableView, canEditRowAtIndexPath indexPath: NSIndexPath) -> Bool {
        // Return false if you do not want the specified item to be editable.
        return true
    }
    */

    /*
    // Override to support editing the table view.
    override func tableView(tableView: UITableView, commitEditingStyle editingStyle: UITableViewCellEditingStyle, forRowAtIndexPath indexPath: NSIndexPath) {
        if editingStyle == .Delete {
            // Delete the row from the data source
            tableView.deleteRowsAtIndexPaths([indexPath], withRowAnimation: .Fade)
        } else if editingStyle == .Insert {
            // Create a new instance of the appropriate class, insert it into the array, and add a new row to the table view
        }    
    }
    */

    /*
    // Override to support rearranging the table view.
    override func tableView(tableView: UITableView, moveRowAtIndexPath fromIndexPath: NSIndexPath, toIndexPath: NSIndexPath) {

    }
    */

    /*
    // Override to support conditional rearranging of the table view.
    override func tableView(tableView: UITableView, canMoveRowAtIndexPath indexPath: NSIndexPath) -> Bool {
        // Return false if you do not want the item to be re-orderable.
        return true
    }
    */

    /*
    // MARK: - Navigation

    // In a storyboard-based application, you will often want to do a little preparation before navigation
    override func prepareForSegue(segue: UIStoryboardSegue, sender: AnyObject?) {
        // Get the new view controller using segue.destinationViewController.
        // Pass the selected object to the new view controller.
    }
    */

}
