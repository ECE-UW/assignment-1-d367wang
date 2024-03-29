import sys

# YOUR CODE GOES HERE
import cmdParser


def main():
    ### YOUR MAIN CODE GOES HERE

    ### sample code to read from stdin.
    ### make sure to remove all spurious print statements as required
    ### by the assignment
    while True:
        # print 'your command: '
        input = sys.stdin.readline().strip('\n')
        # if line == '':
        #     break
        # print 'read a line:', line
        # input = raw_input()
        if input == '':
            break
        try:
            cmdParser.operation_parse(input)
        except Exception as e:
            print 'Error: '+ e.message
        # cmdParser.operation_parse(input)

    # print 'Finished reading input'
    # return exit code 0 on successful termination
    sys.exit(0)


if __name__ == '__main__':
    main()
