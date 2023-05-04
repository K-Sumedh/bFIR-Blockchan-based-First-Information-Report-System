// SPDX-License-Identifier: GPL-3.0

pragma solidity >=0.7.0 <0.9.0;

contract SpActions
{
    struct PoliceStation
    {
        string stationId;
        string Address;
        string policeOfficer;
        string password;
    }

    PoliceStation[] public stationDetails;

    //all police stations list
    string[] public stations;

    mapping(string => string) public stationIdToPassword;

    //function to add police stations
    function AddPoliceStation(string memory _stationId, string memory _Address, string memory _officer, string memory _pwd)
    public
    {
        stationDetails.push(PoliceStation(_stationId, _Address, _officer, _pwd));
        stationIdToPassword[_stationId] = _pwd;
        stations.push(_stationId);
    }

    function UpdatePoliceStationDetails(string memory _stationId, string memory _Address, string memory _officer, string memory _pwd)
    public
    {
        uint256 len = stationDetails.length;
        uint256 i=0;
        for(i=0;i<len;i++)
        {
            if (keccak256(abi.encodePacked(_stationId)) == keccak256(abi.encodePacked(stationDetails[i].stationId)))
            {
                stationDetails[i].Address = _Address;
                stationDetails[i].policeOfficer = _officer;
                stationDetails[i].password = _pwd;

                stationIdToPassword[_stationId] = _pwd;
                break;          
            }
        }
    }

    function getPoliceStationDetails(string memory _psname)
    public view returns (PoliceStation memory)
    {
        uint256 len = stationDetails.length;
        uint256 i=0;
        for(i=0;i<len;i++)
        {
            if(keccak256(abi.encodePacked(_psname)) == keccak256(abi.encodePacked(stationDetails[i].stationId)))
            {
                return stationDetails[i];
            }
        }
        PoliceStation memory emptyObj;
        return emptyObj;
    }
}