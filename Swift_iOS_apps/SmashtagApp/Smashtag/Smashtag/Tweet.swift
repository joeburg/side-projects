//
//  Tweet.swift
//
//
//  Created by Joe Burg  on 12/9/16.
//
//

import CoreData
import Foundation
import Twitter


class Tweet: NSManagedObject
{
    
    // Insert code here to add functionality to your managed object subclass
    
    // make sure the tweet is unique and load it to the database
    class func tweetWithTwitterInfo(twitterInfo: Twitter.Tweet, inManagedObjectContext context: NSManagedObjectContext) -> Tweet? {
        
        // look in the database and see if the tweet already exists
        
        let request = NSFetchRequest(entityName: "Tweet")
        request.predicate = NSPredicate(format: "unique = %@", twitterInfo.id)
        
        // we can reduce this code using optional chaining
        //        do {
        //            // look in the database
        //            let queryResults = try context.executeFetchRequest(request)
        //
        //            // returns first item in array
        //            if let tweet = queryResults.first as? Tweet {
        //                return tweet
        //            }
        //
        //        } catch let error {
        //            // ignore
        //        }
        
        // if you're going to catch and do something then you need to use the verbose way above
        if let tweet = (try? context.executeFetchRequest(request))?.first as? Tweet {
            return tweet
        } else if let tweet = NSEntityDescription.insertNewObjectForEntityForName("Tweet", inManagedObjectContext: context) as? Tweet {
            // if you cant find the tweet, the add it to the database
            tweet.unique = twitterInfo.id
            tweet.text = twitterInfo.text
            tweet.posted = twitterInfo.created
            // automatically adds this tweet to the twitter user model as well
            tweet.tweeter = TwitterUser.twitterUserWithTwitterInfo(twitterInfo.user, inManagedObjectContext: context)
            return tweet
        }
        
        return nil
    }
    
    
}
