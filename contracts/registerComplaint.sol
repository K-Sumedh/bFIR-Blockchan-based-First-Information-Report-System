// SPDX-License-Identifier: GPL-3.0
pragma solidity >=0.7.0 <0.9.0;

contract registerComplaint{
    struct complaint{
        string  id;
        string  docHash;
        string  Name;
        string  date;
        string  time;
        string  state;
        string  district;
        string  policeStation;
        string  mobile;
        string  addres;
        string  description;
        string  complaintTitle;
    }

    uint256 noOfComplaints=0;  //cache for searching
    complaint[] public comp; //array for list of complaints
    mapping(string => uint256) public idToComplaint;

    //UnSolvedStationIdToComplaints[] public unsolved;
    mapping(string => string[]) public stationToCompId;
    
    function  addComplaint(string memory _id, string memory _docHash, string memory _Name,
                            string memory _date, string memory _time, string memory _state, 
                            string memory _district, string memory _stationId,
                            string memory _mobile, string memory _addres, 
                            string memory _description, string memory _complaintTitle)
    public
    {
        comp.push(complaint(_id, _docHash, _Name, _date, _time, _state, _district, _stationId,
                            _mobile, _addres, _description, _complaintTitle));
        
        idToComplaint[_id] = noOfComplaints;
        stationToCompId[_stationId].push(_id);
        noOfComplaints += 1;
    }

    function getComplaint(string memory _id)
    public view returns (complaint memory)
    {
        return comp[idToComplaint[_id]];
    }

    function getComplaintIdsForPolice(string memory _stationId)
    public view returns (string[] memory)
    {
        string[] memory listOfIds = stationToCompId[_stationId];
        return listOfIds;
    }

    function getComplaintsForComplainant(string memory _userId)
    public view returns (complaint[10] memory, uint256)
    {
        complaint[10] memory temp;
        uint256 len = comp.length;
        uint256 i=0;
        uint256 count=0;
        for(i=0;i<len;i++)
        {
            if (keccak256(abi.encodePacked(comp[i].Name)) == keccak256(abi.encodePacked(_userId)))
            {
                temp[count] = comp[i];
                count += 1;
            }
        }
        return (temp, count);
    }
}


