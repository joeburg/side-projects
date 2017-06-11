//
//  ViewController.swift
//  FaceIt
//
//  Created by Joe Burg  on 12/5/16.
//  Copyright © 2016 Joe Burg . All rights reserved.
//

import UIKit

// rename the ViewController to FaceViewController
// also rename to file to FaceViewController - best practice 
// is to name the file by the most important class in that file 
// also be sure to go to the identity inspector section in the storyboard 
// and in the "Custom Class" section change Class to FaceViewController
class FaceViewController: UIViewController
{
    var expression = FacialExpression(eyes: .Closed, eyeBrows: .Relaxed, mouth: .Smile) {
        // if you set a value during initialization, didSet{} is not called 
        // it's only called after initialization
        // so this updates when the model is changed
        didSet {
            updateUI()
        }
    }

    // get a pointer to the face view 
    // this wires up the outlet so it's actually pointing to the faceView
    @IBOutlet weak var faceView: FaceView! {
        // the didSet{} is called after initialization of the faceView so it will update it
        // so this updates after the model is first hooked up
        didSet {
            // add a pinch gesture recognizer
            faceView.addGestureRecognizer(
                UIPinchGestureRecognizer(
                    target: faceView,
                    // note: (_:) means the method has an action
                    action: #selector(FaceView.changeScale(_:))
                ))
            
            // add a swipe gesture recognizer 
            // here the reconizer is handled by the controller since the gesture
            // is going to change the model (the handler will change the model)
            let happierSwipeGestureRecognizer = UISwipeGestureRecognizer(
                target: self,
                action: #selector(FaceViewController.increaseHappiness)
            )
            // set the direction of the swipe
            happierSwipeGestureRecognizer.direction = .Up
            faceView.addGestureRecognizer(happierSwipeGestureRecognizer)
            
            // create a down swipe to make the face sadder 
            let sadderSwipeGestureRecognizer = UISwipeGestureRecognizer(
                target: self,
                action: #selector(FaceViewController.decreaseHappiness)
            )
            sadderSwipeGestureRecognizer.direction = .Down
            faceView.addGestureRecognizer(sadderSwipeGestureRecognizer)
            
            
            // update the UI (Note: important that we have updateUI() in both cases)
            updateUI()
        }
    }

    // we made this gesture recognizer via the storyboard GUI
    // note: changed sender to recognizer since it's a gesture
    // the addGestureRecognizer is added from dragging this from
    // the storyboard
    @IBAction func toggleEyes(recognizer: UITapGestureRecognizer) {
        if recognizer.state == .Ended {
            switch expression.eyes {
            case .Open: expression.eyes = .Closed
            case .Closed: expression.eyes = .Open
            case .Squinting: break
            }
        }
    }
    
    private struct Animation {
        static let ShakeAngle = CGFloat(M_PI/6)
        static let ShakeDuration = 0.5
    }
    
    @IBAction func headShake(sender: UITapGestureRecognizer)
    {
        UIView.animateWithDuration(
            Animation.ShakeDuration,
            animations: {
                self.faceView.transform = CGAffineTransformRotate(self.faceView.transform, Animation.ShakeAngle)
            },
            completion: { finished in
                // animate to move back the other way - chain the animation to go back an forth
                if finished {
                    UIView.animateWithDuration(
                        Animation.ShakeDuration,
                        animations: {
                            self.faceView.transform = CGAffineTransformRotate(self.faceView.transform, -Animation.ShakeAngle*2)
                        },
                        completion: { finished in
                            if finished {
                                UIView.animateWithDuration(
                                    Animation.ShakeDuration,
                                    animations: {
                                        self.faceView.transform = CGAffineTransformRotate(self.faceView.transform, Animation.ShakeAngle)
                                    },
                                    completion: { finished in
                                        if finished {
                                            
                                        }
                                    }
                                )
                            }
                        }
                    )
                }
            }
        )
    }
    
    // handler for the up swipe gesture
    func increaseHappiness()
    {
        // the happierMouth func is in the FacialExpressions model
        expression.mouth = expression.mouth.happierMouth()
    }

    
    // handler for the down swipe gesture 
    func decreaseHappiness()
    {
        // the sadderMouth func is in the FacialExpressions model
        expression.mouth = expression.mouth.sadderMouth()
    }

    
    
    // note: FacialExpression.Mouth is implied for subsequent keys (.Grin, etc.)
    private var mouthCurvatures = [FacialExpression.Mouth.Frown: -1.0,
                                   .Grin: 0.5,
                                   .Smile: 1.0,
                                   .Smirk: -0.5,
                                   .Neutral: 0.0]
    
    private var eyeBrowTilts = [FacialExpression.EyeBrows.Relaxed: 0.5,
                                .Furrowed: -0.5,
                                .Normal: 0.0]
    
    private func updateUI() {
        // IMPORTANT: faceView is an optional and outlets are not set at the time you are preparting 
        // pointers are not set at the time you are preparing so faceView can be nil 
        // can also use faceView?.eyesOpen, faceView?.mouthCurvature, etc. to unwrap the optional
        if faceView != nil {
            switch expression.eyes {
            case .Open: faceView.eyesOpen = true
            case .Closed: faceView.eyesOpen = false
            // note: this is where we interpret the model - is squinting open or closed?
            case .Squinting: faceView.eyesOpen = false
            }
            
            // dictionary returns and optional so you need to set a default
            // ?? 0.0 means you are defaulting it to 0.0 if it returns nil
            faceView.mouthCurvature = mouthCurvatures[expression.mouth] ?? 0.0
            faceView.eyeBrowTilt = eyeBrowTilts[expression.eyeBrows] ?? 0.0
        }
    }
}

