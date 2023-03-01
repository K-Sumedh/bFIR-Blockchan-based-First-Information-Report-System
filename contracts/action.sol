// SPDX-License-Identifier: GPL-3.0

pragma solidity >=0.7.0 <0.9.0;

contract Action
{
    struct ActionFir{
        string cId;
        uint dateTime;
        string comments;
        string actionId;
        string nameOfPolice;
        string actionDocHash;
    }

    struct ActionNcr{
        string cId;
        uint dateTime;
        string comments;
        string actionId;
        string nameOfPolice;
        string actionDocHash;
    }

    enum Progress {COMPLAIN_REGISTERED, FIR_LODGED, NCR_LODGED, UNDER_INVESTIGATION, SOLVED}

    struct complaintProgress{
        string comments;
        Progress progress;
    }

    uint256 noOfFir = 0;
    uint256 noOfNcr = 0;
    ActionFir[] public listOfActionFir;
    ActionNcr[] public listOfActionNcr;

    mapping(string => complaintProgress[]) actionToComments;

    
    //function to lodge an fir/NCR and save it to blockchain
    function TakeAction(bool _isFir, string memory _cid, uint _dateTime, string memory _comments, 
                        string memory _actionId, string memory _nameOfPolice, string memory _actionDocHash,
                        Progress _progress)

    public
    {
        if( _isFir)
        {
            listOfActionFir.push(ActionFir(_cid, _dateTime, _comments, _actionId, _nameOfPolice, _actionDocHash));
            actionToComments[_actionId].push(complaintProgress(_comments, _progress));
            noOfFir = noOfFir + 1;
        }
        else
        {
            listOfActionNcr.push(ActionNcr(_cid, _dateTime, _comments, _actionId, _nameOfPolice, _actionDocHash));
            actionToComments[_actionId].push(complaintProgress(_comments, _progress));
            noOfNcr = noOfNcr + 1;
        }
    }

    //function to update progress of complaint with _actionid and save it to blockchain
    function UpdateProgress(bool _isFir, string memory _actionId, string memory _comments)
    public
    {
        if(_isFir)
        {
            actionToComments[_actionId].push(_comments, actionToComments[_actionId]);
        }
    }

}

