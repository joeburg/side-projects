//
//  TweetersTableViewController.swift
//  Smashtag
//
//  Created by Joe Burg  on 12/9/16.
//  Copyright © 2016 Joe Burg . All rights reserved.
//

import CoreData
import UIKit

class TweetersTableViewController: CoreDataTableViewController {

    // MARK: Model
    
    // user that tweeted the query
    var mention: String? { didSet { updateUI() } }
    // the database
    var managedObjectContext: NSManagedObjectContext? { didSet { updateUI() } }
    
    
    private func updateUI() {
        // glues an NSFetch request to a table 
        // so anytime the database changes, the view will change 
        // the table must sort in the same order as the sectionNameKeyPath
        if let context = managedObjectContext where mention?.characters.count > 0 {
            let request = NSFetchRequest(entityName: "TwitterUser")
            // if mention is nil then it would crash here
            // you should never have something in your public api where if set to nil it crashes
            // this is dealt with above using the where mention? 
            // note: nil is never >, < or = 0
            // the %@ is the same as %s in python; the [c] means case insensitive 
            // we want to make sure that we don't include anyone with darkside in their screenName
            request.predicate = NSPredicate(format: "any tweets.text contains[c] %@ and !screenName beginswith[c] %@", mention!, "darkside")
            // this sorts the queryset by screen name
            request.sortDescriptors = [NSSortDescriptor(
                key: "screenName",
                ascending: true,
                selector: #selector(NSString.localizedCaseInsensitiveCompare(_:))
            )]
            // this makes it case insensitive
            
            
            fetchedResultsController = NSFetchedResultsController(
                fetchRequest: request,
                managedObjectContext: context,
                sectionNameKeyPath: nil,
                cacheName: nil
            )
        } else {
            fetchedResultsController = nil
        }
        

    }
    
    
    private func tweetCountWithMentionByTwitterUser(user: TwitterUser) -> Int?
    {
        var count: Int?
        
        user.managedObjectContext?.performBlockAndWait {
            let request = NSFetchRequest(entityName: "Tweet")
            request.predicate = NSPredicate(format: "text contains[c] %@ and tweeter = %@", self.mention!, user)
            count = user.managedObjectContext?.countForFetchRequest(request, error: nil)
        }
        
        return count
    }
    

    override func tableView(tableView: UITableView, cellForRowAtIndexPath indexPath: NSIndexPath) -> UITableViewCell {
        let cell = tableView.dequeueReusableCellWithIdentifier("TwitterUserCell", forIndexPath: indexPath)

        // Configure the cell...
        if let twitterUser = fetchedResultsController?.objectAtIndexPath(indexPath) as? TwitterUser {
            var screenName: String?
            // since this accesses the database we must use a block
            // notice how we have to perform the block and wait becuase it's asynchronous 
            // and we want to it execute before we update the UI cell which is on the main queue
            twitterUser.managedObjectContext?.performBlockAndWait {
                screenName = twitterUser.screenName
            }
            // this is accessing the UI so it will be on the main queue
            cell.textLabel?.text = screenName
            // add the tweet count by the user 
            if let count = tweetCountWithMentionByTwitterUser(twitterUser) {
                cell.detailTextLabel?.text = (count == 1) ? "1 tweet" : "\(count) tweets"
            } else {
                // if you cant count then just set to empty
                cell.detailTextLabel?.text = ""
            }
            
        }

        return cell
    }



}
