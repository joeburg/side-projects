//
//  EditWaypointViewController.swift
//  Trax
//
//  Created by Joe Burg  on 12/16/16.
//  Copyright © 2016 Joe Burg . All rights reserved.
//

import UIKit

class EditWaypointViewController: UIViewController, UITextFieldDelegate
{

    // MARK: Model
    var waypointToEdit: EditableWaypoint? { didSet { updateUI() } }
    
    
    private func updateUI() {
        nameTextField?.text = waypointToEdit?.name
        infoTextField?.text = waypointToEdit?.info
    }
    
    override func viewDidLoad() {
        super.viewDidLoad()
        // also update the UI here just in case when we are seguing 
        // before our outlets are set we get the UI
        updateUI()
        
        // we dont want the user to have to press the text field 
        // when they get the View, so we automatically start in the 
        // text field and pop up the keyboard
        nameTextField.becomeFirstResponder()
    }
    
    
    // we will use a radio station to update text fields to the waypoint 
    // Note: could also use delegates here to update the waypoint
    
    // these are cookies to keep track of the radio station we are listening to 
    private var ntfObserver: NSObjectProtocol?
    private var itfObserver: NSObjectProtocol?
    
    // use viewDidAppear to start listening to the ratio station
    override func viewDidAppear(animated: Bool) {
        super.viewDidAppear(animated)
        listenToTextFields()
    }
    
    private func listenToTextFields()
    {
        let center = NSNotificationCenter.defaultCenter()
        // do this on the main queue
        let queue = NSOperationQueue.mainQueue()
        
        // start listening to the radio station for the name text
        ntfObserver = center.addObserverForName(
            UITextFieldTextDidChangeNotification,
            object: nameTextField,
            queue: queue)
        { notification in
            if let waypoint = self.waypointToEdit {
                waypoint.name = self.nameTextField.text
            }
        }
        
        // start listening to the radio station for the info text
        itfObserver = center.addObserverForName(
            UITextFieldTextDidChangeNotification,
            object: infoTextField,
            queue: queue)
        { notification in
            if let waypoint = self.waypointToEdit {
                waypoint.info = self.infoTextField.text
            }
        }
    }
    
    // use viewWillDissapear stop listening to the ratio station
    override func viewWillDisappear(animated: Bool) {
        super.viewWillDisappear(animated)
        stopListeningToTextFields()
    }
    
    private func stopListeningToTextFields() {
        if let observer = ntfObserver {
            NSNotificationCenter.defaultCenter().removeObserver(observer)
        }
        
        if let observer = itfObserver {
            NSNotificationCenter.defaultCenter().removeObserver(observer)
        }
    }
    
    // outlets to the Storyboard
    @IBOutlet weak var nameTextField: UITextField! { didSet { nameTextField.delegate = self } }
    @IBOutlet weak var infoTextField: UITextField! { didSet { infoTextField.delegate = self } }
    
    
    /*
    // done button
    @IBAction func done(sender: UIBarButtonItem) {
        self.presentingViewController?.dismissViewControllerAnimated(true, completion: nil)
    }
    */
    
    // remove the keyboard when enter is pressed 
    func textFieldShouldReturn(textField: UITextField) -> Bool {
        textField.resignFirstResponder()
        // no action so it dosnt matter what we return
        return true
    }
}
