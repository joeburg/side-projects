//
//  EmotionsViewController.swift
//  FaceIt
//
//  Created by Joe Burg  on 12/5/16.
//  Copyright © 2016 Joe Burg . All rights reserved.
//

import UIKit

class EmotionsViewController: UIViewController {

    // create a dictionary with the emotions 
    private let emotionalFaces: Dictionary<String,FacialExpression> = [
        "angry" : FacialExpression(eyes: .Closed, eyeBrows: .Furrowed, mouth: .Frown),
        "happy" : FacialExpression(eyes: .Open, eyeBrows: .Normal, mouth: .Smile),
        "worried" : FacialExpression(eyes: .Open, eyeBrows: .Relaxed, mouth: .Smirk),
        "mischievious" : FacialExpression(eyes: .Open, eyeBrows: .Furrowed, mouth: .Grin)
    ]
    
    
    // MARK: - Navigation

    // In a storyboard-based application, you will often want to do a little preparation before navigation
    override func prepareForSegue(segue: UIStoryboardSegue, sender: AnyObject?) {
        // Get the new view controller using segue.destinationViewController.
        // Pass the selected object to the new view controller.
        
        var destinationvc = segue.destinationViewController
        // important: since we embedded the faceviewcontroller in a navigation controller in the storyboard
        // desinationvc can actually be a navigation controller in some cases
        // so for that case we take the view that is inside the navigation controller 
        if let navcon = destinationvc as? UINavigationController {
            // if you cant unwrap it then just keep it the same
            destinationvc = navcon.visibleViewController ?? destinationvc
        }
        
        // can't work with a generic UIViewController, you need the subclass
        // so cast onto FaceViewController which we can work with and change its model
        if let facevc = destinationvc as? FaceViewController {
            // make sure the identifier is not nil
            if let identifier = segue.identifier {
                if let expression = emotionalFaces[identifier] {
                    // note we are setting the face view model's here 
                    // by accessing the expression method in the face view controller
                    facevc.expression = expression
                    
                    // now to use the button's title as the face view's title, user the 
                    // sender to get that info
                    // note: sender is AnyObject so we must cast as a UIButton to do anything
                    if let sendingButton = sender as? UIButton {
                        // navigationItem is a little bundle of information that the 
                        // navitagion controller looks inside of when that view is showing
                        facevc.navigationItem.title = sendingButton.currentTitle
                    }
                }
            }
        }
        
    }
    

}
