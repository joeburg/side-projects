//
//  DropItViewController.swift
//  DropIt
//
//  Created by Joe Burg on 12/10/16.
//  Copyright © 2016 Joe Burg. All rights reserved.
//

import UIKit

class DropItViewController: UIViewController {
    
    // outlet to view in UI 
    @IBOutlet weak var gameView: DropItView! {
        didSet {
            gameView.addGestureRecognizer(UITapGestureRecognizer(target: self, action: #selector(addDrop(_:))))
            gameView.addGestureRecognizer(UIPanGestureRecognizer(target: gameView, action: #selector(DropItView.grabDrop(_:))))
            gameView.realGravity = true 
        }
    }
    
    // add the drop if the state has ended
    func addDrop(recognizer: UITapGestureRecognizer) {
        if recognizer.state == .Ended {
            gameView.addDrop()
        }
    }
    
    
    // turn view on
    override func viewDidAppear(animated: Bool) {
        super.viewDidAppear(animated)
        gameView.animating = true
    }
    
    
    // turn view off
    override func viewWillDisappear(animated: Bool) {
        super.viewWillDisappear(animated)
        gameView.animating = false
    }
}
