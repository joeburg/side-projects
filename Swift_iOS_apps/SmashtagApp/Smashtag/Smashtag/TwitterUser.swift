//
//  TwitterUser.swift
//  
//
//  Created by Joe Burg  on 12/9/16.
//
//

import CoreData
import Foundation
import Twitter



class TwitterUser: NSManagedObject
{

    // Insert code here to add functionality to your managed object subclass

    
    // a class method which
    // returns a TwitterUser from the database if Twitter.User has already been put in
    // or returns a newly-added-to-the-database TwitterUser if not
    
    class func twitterUserWithTwitterInfo(twitterInfo: Twitter.User, inManagedObjectContext context: NSManagedObjectContext) -> TwitterUser?
    {
        let request = NSFetchRequest(entityName: "TwitterUser")
        // the screen name is unique so use that as the unique idenifier 
        request.predicate = NSPredicate(format: "screenName = %@", twitterInfo.screenName)
        if let twitterUser = (try? context.executeFetchRequest(request))?.first as? TwitterUser {
            return twitterUser
        } else if let twitterUser = NSEntityDescription.insertNewObjectForEntityForName("TwitterUser", inManagedObjectContext: context) as? TwitterUser {
            twitterUser.screenName = twitterInfo.screenName
            twitterUser.name = twitterInfo.name
            return twitterUser
        }
        return nil
    }
}

