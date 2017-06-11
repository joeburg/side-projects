//
//  ViewController.swift
//  Calculator
//
//  Created by Joe Burg  on 12/2/16.
//  Copyright © 2016 Joe Burg . All rights reserved.
//

import UIKit

// this gobal variable is to calculate how many calculator MVCs we have
var calculatorCount = 0

class ViewController: UIViewController {
    
    @IBOutlet private weak var display: UILabel!
    
    private var userIsInTheMiddleOfTyping = false
    
    // this code will show that and MVC is created every time we push the calculate button
    override func viewDidLoad() {
        // in the view controller life cycle, you must always call super
        super.viewDidLoad()
        calculatorCount += 1
        print("Loaded up a new Calculator (count = \(calculatorCount))")
        
        // here we add a red square root function; this will be a closure
        // saving this code to rememeber the memory cycle
        //        brain.addUnaryOperation("Z") {
        //            // we have to have a strong pointer here (self) becuase of the
        //            // memory cycle
        //            // when we have this cycle, we begin to collect caclulator MVCs
        //            // in the heap (pay attention to calculator count)
        //            // this would be a big problem is this was a video or someting that
        //            // requries alot of data
        //            self.display.textColor = UIColor.redColor()
        //            return sqrt($0)
        //        }
        
        // fixing the memory cycle issue (pointer pointint to pointer which dosnt leave heap)
        // since 'me' is unowned here it wont remain in the heap
        brain.addUnaryOperation("Z") { [unowned me = self ] in
            me.display.textColor = UIColor.redColor()
            return sqrt($0)
        }
        
        //        // other option is to use a weak optional
        //        brain.addUnaryOperation("Z") { [ weak  weakSelf = self ] in
        //            weakSelf?.display.textColor = UIColor.redColor()
        //            return sqrt($0)
        //        }
    }
    
    // this method (deinit) will tell us when this class leaves the heap
    deinit {
        calculatorCount -= 1
        print("Calculator left the heap (count = \(calculatorCount))")
    }
    
    
    
    @IBAction private func touchDigit(sender: UIButton) {
        let digit = sender.currentTitle!
        
        if userIsInTheMiddleOfTyping {
            let textCurrentlyInDisplay = display.text!
            display.text = textCurrentlyInDisplay + digit
        } else {
            display.text = digit
        }
        userIsInTheMiddleOfTyping = true
    }
    
    // create a property that is calculated so you don't have to
    // consitently convert between a double and string
    // called computed properties
    private var displayValue: Double {
        get {
            // some things can't be converted so use optional Double
            return Double(display.text!)!
        }
        set {
            display.text = String(newValue)
        }
    }
    
    // set is as optional since you havn't hit save yet
    var savedProgram: CalculatorBrain.PropertyList?
    
    @IBAction func save() {
        savedProgram = brain.program
    }
    
    @IBAction func restore() {
        if savedProgram != nil {
            brain.program = savedProgram!
            displayValue = brain.result
        }
    }
    
    // get the controller to talk to the brian model by defining a var
    private var brain = CalculatorBrain()
    
    @IBAction private func performOperation(sender: UIButton) {
        if userIsInTheMiddleOfTyping {
            brain.setOperand(displayValue)
        }
        
        userIsInTheMiddleOfTyping = false
        if let mathematicalSymbol = sender.currentTitle {
            brain.performOperation(mathematicalSymbol)
        }
        displayValue = brain.result
    }
    
}

