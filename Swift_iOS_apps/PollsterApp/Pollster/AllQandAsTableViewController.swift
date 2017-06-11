//
//  AllQandAsTableViewController.swift
//  Pollster
//
//  Created by Joe Burg on 12/15/16.
//  Copyright © 2016 Joe Burg. All rights reserved.
//

import CloudKit
import UIKit

class AllQandAsTableViewController: UITableViewController
{
    // MARK - model
    var allQandAs = [CKRecord]() { didSet { tableView.reloadData() } }
    
    override func viewWillAppear(animated: Bool) {
        super.viewWillAppear(animated)
        fetchAllQandAs()
        
        // subscribe to the QandAs
        iCloudSubscribeToQandAs()
    }
    
    override func viewDidDisappear(animated: Bool) {
        // unsuscribe to the QandAs
        iCloudUnsuscribeToQandAs()
    }
 
    // get the database
    private let database = CKContainer.defaultContainer().publicCloudDatabase
    
    private func fetchAllQandAs() {
        // TRUEPREDICATE means get them all 
        let predicate = NSPredicate(format: "TRUEPREDICATE")
        
        // this is a queryset
        let query = CKQuery(recordType: Cloud.Entity.QandA, predicate: predicate)
        
        // we can sort the query (made this an array)
        query.sortDescriptors = [NSSortDescriptor(key: Cloud.Attribute.Question, ascending: true)]
        
        // ask the database to perform the query
        database.performQuery(query, inZoneWithID: nil) { (records, error) in
            if records != nil {
                // NOTE: query to database does not happend on the main queue
                // but changing the model reloads the data in the table view
                // so we need to put this on the main queue
                dispatch_async(dispatch_get_main_queue()) {
                    self.allQandAs = records!
                }
            }
        }
    }
    
    
    
    
    // MARK - UITableViewDataSource 
    
    // set the number of rows
    override func tableView(tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        return allQandAs.count
    }
    
    // set the cell for row at index path
    override func tableView(tableView: UITableView, cellForRowAtIndexPath indexPath: NSIndexPath) -> UITableViewCell {
        let cell = tableView.dequeueReusableCellWithIdentifier("QandA Cell", forIndexPath: indexPath)
        
        // set the title of the cell
        // note: the Cloud.Attribute.Question comes back as a CKRecord so we have to set it as a string
        //cell.textLabel?.text = allQandAs[indexPath.row][Cloud.Attribute.Question] as? String
        cell.textLabel?.text = allQandAs[indexPath.row].question
        return cell
    }
    
    // we want to allow the user to swipe to delete 
    override func tableView(tableView: UITableView, canEditRowAtIndexPath indexPath: NSIndexPath) -> Bool {
        // only allow users to delete their own Q and As
        return allQandAs[indexPath.row].wasCreatedByThisUser
    }
    
    // this commits the delete 
    override func tableView(tableView: UITableView, commitEditingStyle editingStyle: UITableViewCellEditingStyle, forRowAtIndexPath indexPath: NSIndexPath) {
        if editingStyle == .Delete {
            // delete from table and database
            let record = allQandAs[indexPath.row]
            database.deleteRecordWithID(record.recordID) { (deletedRecord, error) in
                // handle errors
            }
            allQandAs.removeAtIndex(indexPath.row)
        }
    }
    
    
    // MARK - Subscription 
    
    // this allows us to listen to a radio channel to see if changes have been made to the
    // database and the automatically update the UI
    
    private let subscriptionID = "All QandA Creations and Deletions"
    
    // create a cookie for listening to the radio station
    private var cloudKitObserver: NSObjectProtocol?
    
    // make the subscription
    private func iCloudSubscribeToQandAs() {
        // setup a predicate that says what we are looking for 
        // we are looking for any additions or deletions to Q and A
        let predicate = NSPredicate(format: "TRUEPREDICATE")
        let subscription = CKSubscription(
            recordType: Cloud.Entity.QandA,
            predicate: predicate,
            subscriptionID: self.subscriptionID,
            // look for creations and deletions
            options: [.FiresOnRecordCreation, .FiresOnRecordDeletion]
        )
        
        // you can do somethign when the notification occurs 
        // e.g. alerts
        // subscription.notificationInfo = ...
        
        // save the subscription to the database
        database.saveSubscription(subscription) { (savedSubscription, error) in
            // if the subscription is already on the server the it 
            // will reject your reqeust -- this is a common error
            if error?.code == CKErrorCode.ServerRejectedRequest.rawValue {
                // ignore
            } else if error != nil {
                // report error, etc.
            }
        }
        
        // subscribe to the radio station (in app delegate)
        cloudKitObserver = NSNotificationCenter.defaultCenter().addObserverForName(
            CloudKitNotifications.NotificationReceived,
            object: nil,
            queue: NSOperationQueue.mainQueue(),
            usingBlock: { notification in
                if let ckqn = notification.userInfo?[CloudKitNotifications.NotificationKey] as? CKQueryNotification {
                    self.iCloudHandleSubscriptionNotification(ckqn)
                }
            }
        )
    }
    
    private func iCloudHandleSubscriptionNotification(ckqn: CKQueryNotification) {
        // make sure its the right subscription 
        // there may be many stations
        if ckqn.subscriptionID == self.subscriptionID {
            if let recordID = ckqn.recordID {
                // find out what changed 
                switch ckqn.queryNotificationReason {
                case .RecordCreated:
                    // fetch the record
                    database.fetchRecordWithID(recordID) { (record, error) in
                        if record != nil {
                            // you need to put the new record into a sorted list 
                            dispatch_async(dispatch_get_main_queue()) {
                                self.allQandAs = (self.allQandAs + [record!]).sort {
                                    // this sorts the list, but looks messy
                                    // in CloudKitExtensions, we added extensions to CKRecord to clean up the code
                                    // return ($0[Cloud.Attribute.Question] as? String) < $1[Cloud.Attribute.Question] as? String)
                                    // in CloudKitExtensions, we added extensions to CKRecord to clean up the code
                                    return $0.question < $1.question
                                }
                            }
                        }
                        // if you cant fetch the record then you might want to do somethign
                    }
                    
                case .RecordDeleted:
                    dispatch_async(dispatch_get_main_queue()) {
                        // remove the records where don't have the ID
                        self.allQandAs = self.allQandAs.filter { $0.recordID != recordID }
                    }
                default:
                    break
                }
            }
        }
    }
    
    
    
    // also un-subscribe 
    private func iCloudUnsuscribeToQandAs() {
        // we forgot to stop listening to the radio station in the lecture demo!
        // here's how we do that ...
        if let observer = cloudKitObserver {
            NSNotificationCenter.defaultCenter().removeObserver(observer)
            cloudKitObserver = nil
        }

        // delete the subscrition with the database
        database.deleteSubscriptionWithID(self.subscriptionID) { (subscription, error) in
            // handle the errors
        }
    }
    
    
    // MARK - Navigation 
    
    // prepare for the segue between the views 
    override func prepareForSegue(segue: UIStoryboardSegue, sender: AnyObject?) {
        if segue.identifier == "Show QandA" {
            // the MVC we are seguing to is a cloud QandA table view controller
            if let ckQandATVC = segue.destinationViewController as? CloudQandATableViewController {
                
                // note: let indexPath = tableView.indexPathForCell(cell) is a one-liner to get the index 
                // path for the cell that was chosen
                if let cell = sender as? UITableViewCell, let indexPath = tableView.indexPathForCell(cell) {
                    // now we set the controller's public api 
                    ckQandATVC.ckQandARecord = allQandAs[indexPath.row]
                } else {
                    // in the case that we cant get the cell, then it's because we pushed the "+" button
                    // in the all QandAs Table view
                    // so set the public api to a new CKRecord 
                    ckQandATVC.ckQandARecord = CKRecord(recordType: Cloud.Entity.QandA)
                }
            }
        }
    }
    
}
