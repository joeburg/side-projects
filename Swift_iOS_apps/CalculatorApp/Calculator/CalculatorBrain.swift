//
//  CalculatorBrain.swift
//  Calculator
//
//  Created by Joe Burg  on 12/2/16.
//  Copyright © 2016 Joe Burg . All rights reserved.
//

import Foundation


// global functions
//func multiply(op1: Double, op2: Double) -> Double {
//    return op1 * op2
//}

// swift can implement "closures": inline function that captures that state of it's enviornment 
// has the same format as a function but the { starts at the beginning of the expression and then 
// you put 'in' where the { normally starts for a fucntion 
// e.g. { (op1: Double, op2: Double) -> Double in return op1 * op2 }
// you can use type inference to make it look cleaner 
// { (op1, op2) in return op1 * op2 } 
// but you can use defalt variables
// { ($0, $1) in return $0 * $1 }
// but swift will infer the arguements, so you can have 
// { return $0 * $1 } 
// but since $0 * $1 is a double and swift knows it should return a double, you dont need return 
// { $0 * $1 }


class CalculatorBrain
{
    
    private var accumulator = 0.0
    // set an array of AnyObject
    private var internalProgram = [AnyObject]()
    
    
    func setOperand(operand: Double) {
        accumulator = operand
        internalProgram.append(operand)
        // Note: the operand is a double here while internalProgram stores AnyObject
        // this is where the C-briging takes places and stores it accordingly
    }
    
    // this code will allow us to make a red square root function
    func addUnaryOperation(symbol: String, operation: (Double) -> Double) {
        operations[symbol] = Operation.UnaryOperation(operation)
    }
    
    // create a table to reduce code redundancy of the operations
    private var operations: Dictionary<String,Operation> = [
        "π" : Operation.Constant(M_PI),
        "e" : Operation.Constant(M_E),
        "√" : Operation.UnaryOperation(sqrt),
        "cos" : Operation.UnaryOperation(cos),
        "✕" : Operation.BinaryOperation({ $0 * $1 }),
        "÷" : Operation.BinaryOperation({ $0 / $1 }),
        "+" : Operation.BinaryOperation({ $0 + $1 }),
        "−" : Operation.BinaryOperation({ $0 - $1 }),
        "=" : Operation.Equals
    ]
    
    // enum in swift has discrete values (constant, unary operation, BinaryOperation, Equals, etc.)
    // enum in swift can have methods
    // enum cannot have any storage vars
    // enum cannot inherit fron another enum
    // enum is pass by value
    private enum Operation {
        // can provide an associated type for the optional e.g. Constant(Double)
        case Constant(Double)
        // func is a type if swift just like a Double
        // so you can define a function that takes a Double and then returns a Double
        case UnaryOperation((Double) -> Double)
        // the binary operation (e.g. multiply) is a function that takes two doubles and returns a double
        case BinaryOperation((Double, Double) -> Double)
        case Equals
    }
    
    func performOperation(symbol: String) {
        // append the symbol for the operation 
        internalProgram.append(symbol)
        
        
        //switch symbol {
        //case "π": accumulator = M_PI
        //case "√": accumulator = sqrt(accumulator)
        // string has infinite cases so specify a default
        //default: break
        //}
        
        //if  let constant = operations[symbol] {
        //    accumulator = constant
        //}
        
        if let operation = operations[symbol] {
            switch operation {
            // swift implies Operation.Constant when you use .Constant
            case .Constant(let value):
                accumulator = value
            case .UnaryOperation(let function):
                accumulator = function(accumulator)
            case .BinaryOperation(let function):
                executePendingBinaryOperation()
                pending = PendingBinaryOperationInfo(binaryFunction: function, firstOperand: accumulator)
            case .Equals:
                executePendingBinaryOperation()
            }
        }
    }
    
    // want everytime that you use a binary operation to then perform equals
    private func executePendingBinaryOperation() {
        if pending != nil {
            accumulator = pending!.binaryFunction(pending!.firstOperand, accumulator)
            pending = nil
        }
    }
    
    // define an optional struct; you want it to be optional since you only need one if a binary operation is called; otherwise it's nil
    private var pending: PendingBinaryOperationInfo?
    
    
    // define a struct - similar to a class; can have vars (stored and computed), no inheritance, struct (line enums) are pass-by-value whereas class are passed-by-reference
    // pass-by-reference means that tbe thing lives in the heap in main memory, so when you pass it around as a value it means you are passing a pointer to it - so when you give it to someone else, they have the same one you have
    // pass-by-value means that when you pass it, it's copied. types of structs: array, Double, int, String, etc. So if you pass an array to something and then add a value to that array, the value will not be added to that array that was passed.
    private struct PendingBinaryOperationInfo {
        var binaryFunction: (Double, Double) -> Double
        var firstOperand: Double
    }
    
    
    // typealias tells the user here that the AnyObject is also a property list
    typealias PropertyList = AnyObject
    
    var program: PropertyList {
        get {
            return internalProgram
            // note: this is not returning a pointer to our data structure
            // it's returning a copy (it's a value type)
        }
        set {
            // here you are running a new program, so first clear out whatever you had before
            clear()
            // if the program that is given is an array of operands and operations, then proceed
            if let arrayOfOps = newValue as? [AnyObject] {
                for op in arrayOfOps {
                    // if the operand is a double , then set the operand
                    if let operand = op as? Double {
                        setOperand(operand)
                    // otherwise perform the operation if a string is given 
                    } else if let operation = op as? String {
                        performOperation(operation)
                    }
                }
            }
        }
    }
    
    func clear() {
        accumulator = 0.0
        pending = nil
        internalProgram.removeAll()
    }
    
    
    // only set get so i'ts a read-only property
    var result: Double {
        get {
            return accumulator
        }
    }
}
