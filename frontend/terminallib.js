/*
  terminallib/terminallib.js - Terminals library.

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


/*
    Converts a customer into a string.
*/
terminallib.customerToString = function (customer) {
    return customer.company.name + ' (' + customer.id + ')';
};


/*
    Converts an address into text.
*/
terminallib.addressToString = function (address) {
    if (address == null) {
        return '-';
    }

    const items = [];
    let streetHouseNumber = [];

    if (address.street) {
        streetHouseNumber.push(address.street);
    }

    if (address.houseNumber) {
        streetHouseNumber.push(address.houseNumber);
    }

    streetHouseNumber = streetHouseNumber.join(' ');

    if (streetHouseNumber) {
        items.push(streetHouseNumber);
    }

    let zipCodeCity = [];

    if (address.zipCode) {
        zipCodeCity.push(address.zipCode);
    }

    if (address.city) {
        zipCodeCity.push(address.city);
    }

    zipCodeCity = zipCodeCity.join(' ');

    if (zipCodeCity) {
        items.push(zipCodeCity);
    }

    return items.join(', ') || '-';
};
