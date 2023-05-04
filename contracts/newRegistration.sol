// SPDX-License-Identifier: GPL-3.0

pragma solidity >=0.7.0 <0.9.0;

contract userRegistration {
    struct User {
        string userId;
        string username;
        string adhaarId;
        string phoneNumber;
        string password;
        string addresss;
        string signatureHash;
        address ethAddress;
    }

    User[] public users; //array for list of users

    mapping(string => string) public nameToPassword; //used to map name to password, so you can get password using username
    mapping(string => string) public userIdToPassword;
    mapping(address => User) public addressToUser;

    function retrieve() public view returns (User[] memory){
        return users; //retrieve tuple of all contacts
    }

    function addUser(string memory _id, string memory _name, string memory _adhaarId,
                     string memory _phoneNumber, string memory _password, string memory _addresss,
                     string memory _hash, string memory _ethAddress) 
    public
    {
        // users.push(User(_id, _name, _adhaarId,_phoneNumber, _password, _addresss, _hash, _ethAddress)); //append to  Contact[] array
        // nameToPassword[_name] = _password; //use name to get phone number
        // userIdToPassword[_id] = _password;

        addressToUser[msg.sender].signatureHash = _hash;
        addressToUser[msg.sender].ethAddress = msg.sender;

        
    }

}
