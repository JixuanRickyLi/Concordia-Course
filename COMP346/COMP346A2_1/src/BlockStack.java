import java.util.Stack;
import common.*;
/**
 * Class BlockStack
 * Implements character block stack and operations upon it.
 *
 * $Revision: 1.4 $
 * $Last Revision Date: 2019/02/02 $
 *
 * @author Serguei A. Mokhov, mokhov@cs.concordia.ca;
 * Inspired by an earlier code by Prof. D. Probst

 */
class BlockStack
{
    Semaphore mutex = new Semaphore(1);
    /**
     * # of letters in the English alphabet + 2
     */
    public static final int MAX_SIZE = 28;

    /**
     * Default stack size
     */
    private static final int DEFAULT_SIZE = 6;

    /**
     * Current size of the stack
     */
    private int iSize = DEFAULT_SIZE;

    /**
     * Current top of the stack
     */
    private int iTop  = 3;

    /**
     * TASK 1: Stack access counter
     */
    private int accessCounter = 0;

    /**
     * stack[0:5] with four defined values
     */
    private char[] acStack = new char[] {'a', 'b', 'c', 'd', '*', '*'};

    /**
     * Default constructor
     */
    public BlockStack()
    {
    }


    public char[] getAcStack() {
        return acStack;
    }

    /**
     * Supplied size
     */
    public BlockStack(final int piSize)
    {
        if(piSize != DEFAULT_SIZE)
        {
            this.acStack = new char[piSize];

            // Fill in with letters of the alphabet and keep
            // 2 free blocks
            for(int i = 0; i < piSize - 2; i++)
                this.acStack[i] = (char)('a' + i);

            this.acStack[piSize - 2] = this.acStack[piSize - 1] = '*';

            this.iTop = piSize - 3;
            this.iSize = piSize;
        }
    }

    /**
     * Picks a value from the top without modifying the stack
     * @return top element of the stack, char
     */
    public char pick()
    {
//        checkEmpty();
        accessCounter++;
        return this.acStack[this.iTop];
    }

    /**
     * Returns arbitrary value from the stack array
     * @return the element, char
     */
    public char getAt(final int piPosition)
    {

        accessCounter++;
        return this.acStack[piPosition];
    }

    /**
     * Standard push operation
     */
    public void push(final char pcBlock)
    {
// should add the original part or not?
        accessCounter++;
        if(this.iSize == -1){
            this.acStack[++this.iTop] = 'a';
            return;
        }
//        checkFull();
        this.acStack[++this.iTop] = pcBlock;
        System.out.println("push succeed /"+pcBlock+"/");
    }

    /**
     * Standard pop operation
     * @return ex-top element of the stack, char
     */
    public char pop()
    {
        accessCounter++;
//        checkEmpty();
        char cBlock = this.acStack[this.iTop];
        this.acStack[this.iTop--] = '*'; // Leave prev. value undefined
        System.out.println("pop succeed /"+ cBlock +"/");
        return cBlock;
    }

    public int getITop(){
        checkEmpty();
        return this.iTop;
    }

    public int getISize(){
        return this.iSize;
    }

    public int getAccessCounter(){
        return accessCounter;

    }

    public boolean isEmpty(){
        return (this.iTop == -1);
    }
    private void checkEmpty() {
        if (this.isEmpty()) {
            throw new StackSizeException("Stack is empty");
        }
    }
    private void checkFull(){
        if (iSize > DEFAULT_SIZE-1){
            throw new StackSizeException("Stack is full");
        }
    }

     class StackSizeException extends RuntimeException{

        StackSizeException(String s){
            super(s);
        }
    }
}



// EOF
