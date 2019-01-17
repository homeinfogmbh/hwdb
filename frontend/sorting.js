/*
  terminallib/sorting.js - Terminals sorting library.

  (C) 2017 HOMEINFO - Digitale Informationssysteme GmbH

  This library is free software: you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation, either version 3 of the License, or
  (at your option) any later version.

  This library is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.

  You should have received a copy of the GNU General Public License
  along with this library.  If not, see <http://www.gnu.org/licenses/>.

  Maintainer: Richard Neumann <r dot neumann at homeinfo period de>
*/
'use strict';

var terminallib = terminallib || {};
terminallib.sorting = terminallib.sorting || {};


/*
    Compares two nullable values.
    Returns the respective sort order if at
    least one object is null-ish, else null.
*/
terminallib.sorting.compareNull = function (alice, bob) {
    if (alice == null) {
        if (bob == null) {
            return 0;
        }

        return -1;
    }

    if (bob == null) {
        return 1;
    }

    return null;
};


/*
    Compares the size of two objects that may be null.
*/
terminallib.sorting.compareSize = function (alice, bob) {
    const result = terminallib.sorting.compareNull(alice, bob);

    if (result != null) {
        return result;
    }

    if (alice > bob) {
        return 1;
    }

    if (alice < bob) {
        return -1;
    }

    return 0;
};


/*
    Compares two addresses.
*/
terminallib.sorting.compareAddress = function (alice, bob) {
    let result = terminallib.sorting.compareNull(alice, bob);

    if (result != null) {
        return result;
    }

    result = terminallib.sorting.compareSize(alice.zipCode, bob.zipCode);

    if (result != 0) {
        return result;
    }

    result = terminallib.sorting.compareSize(alice.city, bob.city);

    if (result != 0) {
        return result;
    }

    result = terminallib.sorting.compareSize(alice.street, bob.street);

    if (result != 0) {
        return result;
    }

    return terminallib.sorting.compareSize(alice.houseNumber, bob.houseNumber);
};


/*
    Returns a sort function to sort by terminal ID.
*/
terminallib.sorting.sortByTID = function (descending) {
    return function (alice, bob) {
        const result = alice.tid - bob.tid;
        return descending ? -result : result;
    };
};


/*
    Returns a sort function to sort by customer ID.
*/
terminallib.sorting.sortByCID = function (descending) {
    return function (alice, bob) {
        const result = alice.customer.id - bob.customer.id;
        return descending ? -result : result;
    };
};


/*
    Returns a sort function to sort by customer name.
*/
terminallib.sorting.sortByCustomerName = function (descending) {
    return function (alice, bob) {
        let result = 0;

        if (alice.customer.company.name > bob.customer.company.name) {
            result = 1;
        } else if (alice.customer.company.name < bob.customer.company.name) {
            result = -1;
        }

        return descending ? -result : result;
    };
};


/*
    Returns a compare function to sort by address.
*/
terminallib.sorting.sortByAddress = function (descending) {
    return function (alice, bob) {
        const result = terminallib.sorting.compareAddress(alice.address, bob.address);
        return descending ? -result : result;
    };
};


/*
    Returns a compare function to sort by deployment date.
*/
terminallib.sorting.sortByDeployed = function (descending) {
    return function (alice, bob) {
        const result = terminallib.sorting.compareSize(alice.deployed, bob.deployed);
        return descending ? -result : result;
    };
};


/*
    Returns a compare function to sort by testing flag.
*/
terminallib.sorting.sortByTesting = function (descending) {
    return function (alice, bob) {
        const result = terminallib.sorting.compareSize(alice.testing, bob.testing);
        return descending ? -result : result;
    };
};


/*
    Returns an appropriate sorting function.
*/
terminallib.sorting.getSorter = function (field, descending) {
    if (field == null) {
        return null;
    }

    switch (field.toLowerCase()) {
    case 'tid':
        return terminallib.sorting.sortByTID(descending);
    case 'cid':
        return terminallib.sorting.sortByCID(descending);
    case 'customer':
        return terminallib.sorting.sortByCustomerName(descending);
    case 'address':
        return terminallib.sorting.sortByAddress(descending);
    case 'deployed':
        return terminallib.sorting.sortByDeployed(descending);
    case 'testing':
        return terminallib.sorting.sortByTesting(descending);
    }

    return null;
};
