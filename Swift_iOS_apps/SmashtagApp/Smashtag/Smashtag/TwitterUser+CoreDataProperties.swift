//
//  TwitterUser+CoreDataProperties.swift
//  
//
//  Created by Joe Burg  on 12/9/16.
//
//
//  Choose "Create NSManagedObject Subclass…" from the Core Data editor menu
//  to delete and recreate this implementation file for your updated model.
//

import Foundation
import CoreData

extension TwitterUser {

    @NSManaged var screenName: String?
    @NSManaged var name: String?
    @NSManaged var tweets: NSSet?

}
