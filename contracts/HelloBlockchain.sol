pragma solidity >=0.4.25 <0.9.0;

contract HelloBlockchain {
    enum StateType { Request }

    StateType public State;
    address public Requestor;
    string public RequestMessage;

    // Declare the event
    event RequestSent(address indexed requestor, string requestMessage, StateType state);

    constructor(string memory message) {
        Requestor = msg.sender;
        RequestMessage = message;
        State = StateType.Request;
    }

    // Call this function to send a request
    function SendRequest(string memory requestMessage) public {
        if (Requestor != msg.sender) {
            revert();
        }

        RequestMessage = requestMessage;
        State = StateType.Request;

        // Emit the event
        emit RequestSent(msg.sender, requestMessage, State);
    }
}

// pragma solidity >=0.4.25 <0.9.0;

// contract HelloBlockchain {
//     //enum StateType { Request, Respond }
// 	enum StateType {Request}

//     StateType public  State;
//     address public  Requestor;
//     //address public  Responder;

//     string public RequestMessage;
//     //string public ResponseMessage;

//     constructor(string memory message) {
//         Requestor = msg.sender;
//         RequestMessage = message;
//         State = StateType.Request;
//     }

//     // call this function to send a request
//     function SendRequest(string memory requestMessage) public {

//         if (Requestor != msg.sender) {
//             revert();
//         }

//         RequestMessage = requestMessage;
//         State = StateType.Request;
//     }

    // // call this function to send a response
    // function SendResponse(string memory responseMessage) public {

    //     Responder = msg.sender;
    //     ResponseMessage = responseMessage;
    //     State = StateType.Respond;
    // }
//}
