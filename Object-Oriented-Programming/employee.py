# Tagle, Marc Neil V.

class Employee:
    def __init__(self, name:str, gender:str, bdate:str, position:str, rate:int, dayswork:int):
        self._name = name
        self._gender = gender
        self._bdate = bdate
        self._position = position
        self._rate = rate
        self._dayswork = dayswork

    def getName(self) -> str:
        return self._name
    
    def getGender(self) -> str:
        return self._gender
    
    def getBdate(self) -> str:
        return self._bdate
    
    def getPosition(self) -> str:
        return self._position
    
    def getRate(self) -> int:
        return self._rate
    
    def getDayswork(self) -> int:
        return self._dayswork
    
    def setName(self, name) -> None:
        self._name = name

    def setGender(self, gender) -> None:
        self._gender = gender

    def setBdate(self, bdate) -> None:
        self._bdate = bdate

    def setPosition(self, position) -> None:
        self._position = position

    def setRate(self, rate) -> None:
        self._rate = rate

    def setDayswork(self, dayswork) -> None:
        self._dayswork = dayswork

    def getGross(self) -> int:
        return self._dayswork * self._rate

    def getSSS(self) -> int:
        gross = self.getGross()
        if gross < 10000:
            return 500
        elif gross <= 20000:
            return 1000
        return 1500
    
    def getTax(self) -> float:
        gross = self.getGross()
        if gross < 10000:
            return 0
        elif gross < 20000:
            return gross * 0.10
        elif gross <= 30000:
            return gross * 0.20
        return gross * 0.25  

    def getNetSalary(self) -> float:
        return self.getGross() - self.getSSS() - self.getTax()

    def getEmployeeDetails(self) -> None:
        print("Employee Details:")
        print(f"Name: {self._name}")
        print(f"Gender: {self._gender}")
        print(f"Birth Date: {self._bdate}")
        print(f"Position: {self._position}")
    
    def getSalaryDetails(self) -> None:
        print("Salary Details:")
        print(f"Gross Salary: P {self.getGross():,.2f}")
        print(f"SSS: P {self.getSSS():,.2f}")
        print(f"Tax: P {self.getTax():,.2f}")
        print(f"Net Salary: P {self.getNetSalary():,.2f}")