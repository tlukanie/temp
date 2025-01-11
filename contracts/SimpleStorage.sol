pragma solidity >=0.6.0 <0.9.0;

contract SimpleStorage {
    uint256 public Salary;

    // Event to emit when Salary is updated
    event SalaryUpdated(uint256 oldSalary, uint256 newSalary);

    // Struct definition
    struct Employee {
        uint256 Salary;
        string name;
    }

    // Array to store employees
    Employee[] public employees;

    // Mapping from name to salary
    mapping(string => uint256) public nameToSalary;

    // Function to store a salary
    function store(uint256 _Salary) public {
        uint256 oldSalary = Salary; // Store the current Salary value
        Salary = _Salary; // Update the Salary variable
        emit SalaryUpdated(oldSalary, _Salary); // Emit the event
    }

    // Function to retrieve the salary
    function retrieve() public view returns (uint256) {
        return Salary;
    }

    // Function to add employees
    function addEmployee(string memory _name, uint256 _Salary) public {
        employees.push(Employee(_Salary, _name));
        nameToSalary[_name] = _Salary;
    }
}


// pragma solidity >=0.6.0 <0.9.0;

// contract SimpleStorage {
//     uint256 public Salary;

//     // This is a comment!

//     struct Employee {
//         uint256 Salary;
//         string name;
//     }

//     Employee[] public employees; // Corrected the array declaration
//     mapping(string => uint256) public nameToSalary;

//     // Function to store a salary
//     function store(uint256 _Salary) public {
//         Salary = _Salary;
//     }

//     // Function to retrieve the salary
//     function retrieve() public view returns (uint256) {
//         return Salary;
//     }

//     // Function to add employees
//     function addEmployee(string memory _name, uint256 _Salary) public {
//         employees.push(Employee(_Salary, _name));
//         nameToSalary[_name] = _Salary;
//     }
// }
