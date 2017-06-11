//
//  CloudQandATableViewController.swift
//  Pollster
//
//  Created by Joe Burg on 12/11/16.
//  Copyright © 2016 Joe Burg. All rights reserved.
//

import CloudKit
import UIKit

class CloudQandATableViewController: QandATableViewController
{
    
    // when you want your public api to be non-optional but you do want 
    // internally the object to be optional use the ckQandARecord and _ckQandARecord
    var ckQandARecord: CKRecord {
        get {
            if _ckQandARecord == nil {
                _ckQandARecord = CKRecord(recordType: Cloud.Entity.QandA)
            }
            return _ckQandARecord!
        }
        set {
            _ckQandARecord = newValue
        }
    }
    
    private var _ckQandARecord: CKRecord? {
        didSet {
            let question = ckQandARecord[Cloud.Attribute.Question] as? String ?? ""
            let answer = ckQandARecord[Cloud.Attribute.Answers] as? [String] ?? []
            qanda = QandA(question: question, answers: answer)
            
            asking = ckQandARecord.wasCreatedByThisUser
        }
    }
    
    
    // this inherits from QandATableViewController which in turn inherits from UITextViewDelegate 
    // so we can use a UITextViewDelegate to update the user's Q and A to the cloud once they have 
    // finished typing 
    override func textViewDidEndEditing(textView: UITextView) {
        super.textViewDidEndEditing(textView)
        iCloudUpdate()
    }
    
    // here we write the method to update the iCloud
    // we must expose it to objective-C
    // the reason it was not initally exposed was because it's private 
    // so either make it public or use @objc
    @objc private func iCloudUpdate()
    {
        // we dont want to put empty questions and answers in the cloud
        if !qanda.question.isEmpty && !qanda.answers.isEmpty {
            ckQandARecord[Cloud.Attribute.Question] = qanda.question
            ckQandARecord[Cloud.Attribute.Answers] = qanda.answers
            iCloudSaveRecord(ckQandARecord)
        }
    }
    
    // method that actually saves it to the cloud
    private func iCloudSaveRecord(recordToSave: CKRecord) {
        database.saveRecord(recordToSave) { (savedRecord, error) in
            // possible errors (note many more)
            // this error is for a record that has been saved newer by someone else
            if error?.code == CKErrorCode.ServerRecordChanged.rawValue {
                // this is called optomistic locking
                // ignore since we want the newer save
            } else if error != nil {
                // re-try; this error could come from network latency 
                self.retryAfterError(error, withSelector: #selector(self.iCloudUpdate))
            }
        }
    }
    
    // this will try to submit again after a set time interval
    private func retryAfterError(error: NSError?, withSelector selector: Selector) {
        // we are calling retryAfterError in a closure that is executed off the main queue
        // important: cannot do NSTImers off the main thread
        // so we need multithreading to call NSTimer on the main queue
        if let retryInterval = error?.userInfo[CKErrorRetryAfterKey] as? NSTimeInterval {
            dispatch_async(dispatch_get_main_queue()) {
                NSTimer.scheduledTimerWithTimeInterval(
                    retryInterval,
                    target: self,
                    selector: selector,
                    userInfo: nil,
                    repeats: false
                )
            }
        }
    }
    
    
    
    // anytime we want to save something to the cloud, we need a database
    // save to the public cloud so everyone can see the others questions 
    private let database = CKContainer.defaultContainer().publicCloudDatabase
    
    
    // if we use this then it always sets the view to nil
    //    override func viewDidLoad() {
    //        super.viewDidLoad()
    //        ckQandARecord = CKRecord(recordType: Cloud.Entity.QandA)
    //    }

}
