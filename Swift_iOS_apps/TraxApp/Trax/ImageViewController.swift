//
//  ImageViewController.swift
//  Cassini
//
//  Created by Joe Burg  on 12/6/16.
//  Copyright © 2016 Joe Burg . All rights reserved.
//

import UIKit

class ImageViewController: UIViewController, UIScrollViewDelegate {
    
    // the model is an image
    var imageURL: NSURL? {
        didSet {
            image = nil
            
            // how to tell if we are on screen
            if view.window != nil {
                fetchImage()
            }
            
        }
    }
    
    // this methods allows you to grab any image given a url
    private func fetchImage() {
        if let url = imageURL {
            
            // just before you dispatch the large job, begin the spinner
            spinner?.startAnimating()
            
            // user an asynchronous dispatch to implement multithreading to load 
            // the very large image 
            // use the initiated queue 
            // for the block closure use trailing form since dispatch takes no arguments and returns no arguments
            // if the last argument of any function is a closure then you can put it outside the ()
            dispatch_async(dispatch_get_global_queue(QOS_CLASS_USER_INITIATED, 0)) {
                let contentsOfURL = NSData(contentsOfURL: url)
                dispatch_async(dispatch_get_main_queue()) {
                    
                    // check to make sure that the url your fetching is the image url
                    // this is important becuase the user could have click another button while this was procesing 
                    if url == self.imageURL {
                        if let imageData = contentsOfURL {
                            // closure wants us to make sure that this is being captured and kept in the heap
                            self.image = UIImage(data: imageData)
                        } else {
                            // also stop the spinner here just in case the user exits the MVC before 
                            // the image is actually loaded
                            self.spinner?.stopAnimating()
                        }
                    } else {
                        print("ignored data returned from url \(url)")
                    }

                }

            }
        }
    }
    
    // scroll view created with the story board
    @IBOutlet weak var scrollView: UIScrollView!
    {
        didSet {
            // make sure to add the content size here as well
            // in the case that the image is crated before 
            // the scroll view is initialized
            scrollView.contentSize = imageView.frame.size
            
            // need to set ourselves as the scroll view's delegate 
            // to use delegate, be sure to give the type of the class UIScrollViewDelegate
            scrollView.delegate = self
            
            // set the scroll view's scale 
            scrollView.minimumZoomScale = 0.03
            scrollView.maximumZoomScale = 1.0
        }
    }
    
    
    // add the spinner from the storyboard 
    @IBOutlet weak var spinner: UIActivityIndicatorView!
    
    
    //
    func viewForZoomingInScrollView(scrollView: UIScrollView) -> UIView? {
        return imageView
    }
    
    
    // instead of creating with view with the storyboard GUI, we will use code here
    private var imageView = UIImageView()
    
    private var image: UIImage? {
        get {
            return imageView.image
        }
        set {
            // note this is stored elsewhere in the imageView
            // but it does intervene when the image size is set
            imageView.image = newValue
            // size the image view to fit whatever image is in it
            imageView.sizeToFit()
            
            // IMPORTANT: we must add the content size of the scroll view
            // note: the scroll view is an outlet so you want to have it
            // as an optional in the case that someone is tries seguing before
            // it's initialized
            scrollView?.contentSize = imageView.frame.size
            
            // once the image has been set, you can stop the spinner 
            spinner?.stopAnimating()
        }
    }
    
    // this method is sent when you're about to appear on screen 
    // this is where you want to send expensive tasks
    override func viewWillAppear(animated: Bool) {
        super.viewWillAppear(animated)
        if image == nil {
            fetchImage()
        }
    }
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        // Do any additional setup after loading the view.
        
        // adding the image view
        //        view.addSubview(imageView)
        // we want the image to be a subview of the scroll view
        scrollView.addSubview(imageView)
        
        
        
        
        // in the demo url code, stanford image is a string
        // the url need to be an object so we use the NSURL to
        // make the string url into an object url
        //imageURL = NSURL(string: DemoURL.Stanford)
        
        // this image gives an error because the app security
        // only allows https urls (not http). So to allow this
        // url you need to add it to the info.plist
        // right click -> Add Row -> App Transport Security Settings
        // click +  -> Allow Arbitrary Loads  YES
        //
    }
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    //    override func didReceiveMemoryWarning() {
    //        super.didReceiveMemoryWarning()
    //        // Dispose of any resources that can be recreated.
    //    }
    
    
    /*
     // MARK: - Navigation
     
     // In a storyboard-based application, you will often want to do a little preparation before navigation
     override func prepareForSegue(segue: UIStoryboardSegue, sender: AnyObject?) {
     // Get the new view controller using segue.destinationViewController.
     // Pass the selected object to the new view controller.
     }
     */
    
}
