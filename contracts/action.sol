// SPDX-License-Identifier: GPL-3.0

pragma solidity >=0.7.0 <0.9.0;

contract Action
{
    struct ActionFir{
        string cId;
        string dateTime;
        string comments;
        uint256 actionId;
        string nameOfPolice;
        string actionDocHash;
    }

    struct ActionNcr{
        string cId;
        string dateTime;
        string comments;
        uint256 actionId;
        string nameOfPolice;
        string actionDocHash;
    }

    enum Progress {COMPLAIN_REGISTERED, FIR_LODGED, NCR_LODGED, UNDER_INVESTIGATION, SOLVED}

    struct complaintProgress{
        string comments;
        Progress progress;
        string dateTime;
    }

    uint256 noOfFir = 0;
    uint256 noOfNcr = 0;
    uint256 actionId = 0;
    ActionFir[] public listOfActionFir;
    ActionNcr[] public listOfActionNcr;

    //mapping of cid to all the actionids
    mapping(string => uint256[]) cIdToAllActionIds;

    mapping(uint256 => complaintProgress[]) actionToComments;

    //list of all cids
    string[] public allCids;

    function getStatusCountForStationId(string[] memory _listOfCids)
    public view returns (uint256[4] memory)
    {
        uint256 i = 0;
        uint256[4] memory ans;
        uint256 status;
        ans[0] = _listOfCids.length;
        for(i=0;i<ans[0];i++)
        {
            uint256[] memory allActionIds = cIdToAllActionIds[_listOfCids[i]];
            uint256 len = allActionIds.length;
            status =  uint256(actionToComments[allActionIds[len-1]][0].progress);

            if (status == 1 || status == 2) { ans[1]++; }
            else if( status == 3 ) { ans[2]++; }
            else if(status == 4) ans[3]++;
        }

        return (ans);
    }
    function getGeneralStatusCounts()
    public view returns (uint256[4] memory)
    {
        uint256[4] memory ans;
        ans[0] = allCids.length;
        uint256 i =0;
        uint256 status;

        for(i=0;i<ans[0];i++)
        {
            uint256[] memory allActionIds = cIdToAllActionIds[allCids[i]];
            uint256 len = allActionIds.length;
            status =  uint256(actionToComments[allActionIds[len-1]][0].progress);

            if (status == 1 || status == 2) { ans[1]++; }
            else if( status == 3 ) { ans[2]++; }
            else if(status == 4) ans[3]++;
        }
        return (ans);
    }

    //function to lodge an fir/NCR and save it to blockchain
    function TakeAction(string memory _isFir, string memory _cid, string memory _dateTime, string memory _comments, 
                        string memory _nameOfPoliceStation, string memory _actionDocHash, Progress _progress)

    public
    {
        if (uint256(_progress) == 0) { allCids.push(_cid); }
        if(keccak256(abi.encodePacked(_isFir)) == keccak256(abi.encodePacked("1"))) //complaint is FIR
        {
            listOfActionFir.push(ActionFir(_cid, _dateTime, _comments, actionId, _nameOfPoliceStation, _actionDocHash));
            actionToComments[actionId].push(complaintProgress(_comments, _progress, _dateTime));
            noOfFir = noOfFir + 1;

            //ading actionid to dictionary of cid to actionid
            cIdToAllActionIds[_cid].push(actionId);

            actionId = actionId + 1;
        }
        else if (keccak256(abi.encodePacked(_isFir)) == keccak256(abi.encodePacked("2"))) //complaint is NCR
        {
            listOfActionNcr.push(ActionNcr(_cid, _dateTime, _comments, actionId, _nameOfPoliceStation, _actionDocHash));
            actionToComments[actionId].push(complaintProgress(_comments, _progress,_dateTime));
            noOfNcr = noOfNcr + 1;

            //ading actionid to dictionary of cid to actionid
            cIdToAllActionIds[_cid].push(actionId);

            actionId = actionId + 1;
        }
    }

    //function to update progress of complaint and save it to blockchain
    function UpdateProgress( string memory _cid, string memory _comments, Progress  _progress, string memory _dateTime)
    public
    {
        if (uint256(_progress) == 0) { allCids.push(_cid); }
        complaintProgress memory cp;
        cp.comments = _comments;
        cp.progress = _progress;
        cp.dateTime = _dateTime;
        actionToComments[actionId].push(cp);

        //ading actionid to dictionary of cid to actionid
        cIdToAllActionIds[_cid].push(actionId);

        actionId = actionId + 1;
    }

    //function get all the actions taken on specific cid
    function getAllActions(string memory _cid)
    public view returns (complaintProgress[][] memory)
    {
        uint256[] memory allActionIds = cIdToAllActionIds[_cid];
        uint256 len = allActionIds.length;
        uint256 i=0;
        complaintProgress[][] memory ans = new complaintProgress[][](len);
        
        for(i=0;i<len;i++){
            ans[i] = actionToComments[allActionIds[i]];
        }
        
        return ans;
    }
}