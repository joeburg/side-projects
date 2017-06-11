//
//  CassiniViewController.swift
//  Cassini
//
//  Created by Joe Burg  on 12/6/16.
//  Copyright © 2016 Joe Burg . All rights reserved.
//

import UIKit

class CassiniViewController: UIViewController, UISplitViewControllerDelegate {
    
    // create a private struct to store the strings in a storyboard
    private struct Storyboard {
        static let ShowImageSegue = "Show Image"
    }
    
    // MARK: - Navigation
    
    // In a storyboard-based application, you will often want to do a little preparation before navigation
    override func prepareForSegue(segue: UIStoryboardSegue, sender: AnyObject?) {
        // Get the new view controller using segue.destinationViewController.
        // Pass the selected object to the new view controller.
        
        
        // good to check the idenifier first since you usually have multiple segues
        if segue.identifier == Storyboard.ShowImageSegue {
            // get the MVC we are seguing to so we can prepare it
            if let ivc = segue.destinationViewController.contentViewController as? ImageViewController {
                
                // we can clean up this code by using and optional
                //                if let sendingButton = sender as? UIButton {
                //                    let imageName = sendingButton.currentTitle
                //                }
                let imageName = (sender as? UIButton)?.currentTitle
                
                // get the image that goes with the button's title 
                ivc.imageURL = DemoURL.NASAImageNamed(imageName)
                ivc.title = imageName
            }
        }
    }
    
    // use target action to get the buttons to work (no segue here)
    // this is used for and ipad split view
    @IBAction func showImage(sender: UIButton) {
        // can only do this in a split view (detail is the last view)
        if let ivc = splitViewController?.viewControllers.last?.contentViewController as? ImageViewController {
            let imageName = sender.currentTitle
            ivc.imageURL = DemoURL.NASAImageNamed(imageName)
            ivc.title = imageName
        } else {
            // now we build a sugue (this is for iphone)
            performSegueWithIdentifier(Storyboard.ShowImageSegue, sender: sender)
        }
    }
    
    
    // we are going to make a split view delegate here to deal with the case where
    // the first page you see is an empty cassini page with a tab going back to the main buttons
    // we want the buttons to show first 
    override func viewDidLoad() {
        super.viewDidLoad()
        splitViewController?.delegate = self
    }
    
    // you don't want the detail to collapse onto the master if the detail is empty
    func splitViewController(splitViewController: UISplitViewController, collapseSecondaryViewController secondaryViewController: UIViewController, ontoPrimaryViewController primaryViewController: UIViewController) -> Bool
    {
        // we are setting the delegate to be our self
        if primaryViewController.contentViewController == self {
            // we want the case where the detail view is nil (no image yet) to not collapse on the master 
            if let ivc = secondaryViewController.contentViewController as? ImageViewController where ivc.imageURL == nil {
                // here we are telling the system that we collapsed the detail onto the master even though we didn't
                return true
            }
        }
        return false
    }
    
}

// extension of UIViewController to allow us to get the content inside 
// a Nagivation controller (this is when we are trying to reconcile split 
// view for ipad and navigation view for iphone and we have a segue to the 
// navigation view in the split view (will give the title)
extension UIViewController {
    var contentViewController: UIViewController {
        if let navcon = self as? UINavigationController {
            return navcon.visibleViewController ?? self
        } else {
            return self
        }
    }
}