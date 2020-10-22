/*
  terminallib/sorting.js - Terminals sorting library.

  (C) 2017-2020 HOMEINFO - Digitale Informationssysteme GmbH

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

import { includesIgnoreCase } from 'https://javascript.homeinfo.de/lib.mjs';
import { addressToString } from 'https://javascript.homeinfo.de/mdb.mjs';


/*
    Compares two nullable values.
    Returns the respective sort order if at
    least one object is null-ish, else null.
*/
function compareNull (alice, bob) {
    if (alice == null) {
        if (bob == null)
            return 0;

        return -1;
    }

    if (bob == null)
        return 1;

    return null;
}


/*
    Compares two addresses.
*/
function compareAddress (alice, bob) {
    let result = compareNull(alice, bob);

    if (result != null)
        return result;

    result = compareSize(alice.zipCode, bob.zipCode);

    if (result != 0)
        return result;

    result = compareSize(alice.city, bob.city);

    if (result != 0)
        return result;

    result = compareSize(alice.street, bob.street);

    if (result != 0)
        return result;

    return compareSize(alice.houseNumber, bob.houseNumber);
}


/*
    Compares the size of two objects that may be null.
*/
function compareSize (alice, bob) {
    const result = compareNull(alice, bob);

    if (result != null)
        return result;

    if (alice > bob)
        return 1;

    if (alice < bob)
        return -1;

    return 0;
}


/*
    Extracts the ID from a filter keyword.
*/
function extractId (keyword) {
    let fragments = null;

    if (keyword.startsWith('#')) {
        fragments = keyword.split('#');
        return parseInt(fragments[1]);
    }

    if (keyword.endsWith('!')) {
        fragments = keyword.split('!');
        return parseInt(fragments[0]);
    }

    return null;
}


/*
    Matches a deployment.
*/
function matchDeployment (deployment, keyword) {
    const cid = '' + deployment.customer.id;

    if (includesIgnoreCase(cid, keyword))
        return true;

    const customerName = deployment.customer.company.name;

    if (includesIgnoreCase(customerName, keyword))
        return true;

    const address = addressToString(deployment.address);

    if (includesIgnoreCase(address, keyword))
        return true;

    return false;
}


/*
    Returns a compare function to sort by address.
*/
function sortByAddress (descending) {
    return function (alice, bob) {
        const result = terminallib.sorting.compareAddress(alice.address, bob.address);
        return descending ? -result : result;
    };
}


/*
    Returns a sort function to sort by customer ID.
*/
function sortByCID (descending) {
    return function (alice, bob) {
        const result = alice.customer.id - bob.customer.id;
        return descending ? -result : result;
    };
}


/*
    Returns a sort function to sort by customer name.
*/
function sortByCustomerName (descending) {
    return function (alice, bob) {
        let result = 0;

        if (alice.customer.company.name > bob.customer.company.name)
            result = 1;
        else if (alice.customer.company.name < bob.customer.company.name)
            result = -1;

        return descending ? -result : result;
    };
}


/*
    Returns a sort function to sort by terminal ID.
*/
function sortByID (descending) {
    return function (alice, bob) {
        const result = alice.id - bob.id;
        return descending ? -result : result;
    };
}


/*
    Returns a compare function to sort by testing flag.
*/
function sortByTesting (descending) {
    return function (alice, bob) {
        const result = compareSize(alice.testing, bob.testing);
        return descending ? -result : result;
    };
}


/*
    Returns the respective deployment as a one-line string.
*/
export function deploymentToString (deployment) {
    return deployment.id + ': ' + addressToString(deployment.address);
}


/*
    Filters the provided depoloyments by the respective keyword.
*/
export function *filterDeployments (deployments, keyword) {
    const id = extractId(keyword);

    for (const deployment of deployments) {
        // Yield any deployment on empty keyword.
        if (keyword == null || keyword == '') {
            yield deployment;
            continue;
        }

        // Exact ID matching.
        if (id != null && id != NaN) {
            if (deployment.id == id)
                yield deployment;

            continue;
        }

        if (matchDeployment(deployment, keyword))
            yield deployment;
    }
}


/*
    Filters the provided systems by the respective keyword.
*/
export function *filterSystems (systems, keyword) {
    const id = extractId(keyword);

    for (const system of systems) {
        // Yield any copy on empty keyword.
        if (keyword == null || keyword == '') {
            yield system;
            continue;
        }

        // Exact ID matching.
        if (id != null && id != NaN) {
            if (system.id == id)
                yield system;

            continue;
        }

        let deployment = system.deployment;

        if (deployment == null)
            continue;

        if (matchDeployment(deployment, keyword))
            yield system;
    }
}


/*
    Returns an appropriate sorting function.
*/
export function getSorter (field, descending) {
    if (field == null)
        return null;

    switch (field.toLowerCase()) {
    case 'id':
        return sortByID(descending);
    case 'cid':
        return sortByCID(descending);
    case 'customer':
        return sortByCustomerName(descending);
    case 'address':
        return sortByAddress(descending);
    case 'testing':
        return sortByTesting(descending);
    }

    return null;
}
