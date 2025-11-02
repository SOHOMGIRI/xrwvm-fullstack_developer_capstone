import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";

function Dealers() {
  const [dealers, setDealers] = useState([]);
  const [stateFilter, setStateFilter] = useState("");

  useEffect(() => {
    const fetchDealers = async () => {
      try {
        const endpoint = stateFilter
          ? `/djangoapp/get_dealers/?state=${stateFilter}`
          : `/djangoapp/get_dealers/`;
        const response = await fetch(endpoint);
        const data = await response.json();
        console.log("Fetched dealers:", data);
        setDealers(data);
      } catch (error) {
        console.error("Error fetching dealers:", error);
      }
    };
    fetchDealers();
  }, [stateFilter]);

  return (
    <div>
      <h2>Dealerships</h2>
      <label>Filter by State: </label>
      <select
        value={stateFilter}
        onChange={(e) => setStateFilter(e.target.value)}
      >
        <option value="">All</option>
        <option value="CA">California</option>
        <option value="TX">Texas</option>
        <option value="NY">New York</option>
      </select>

      {Array.isArray(dealers) && dealers.length > 0 ? (
        <table>
          <thead>
            <tr>
              <th>Name</th>
              <th>City</th>
              <th>State</th>
              <th>Review</th>
            </tr>
          </thead>
          <tbody>
            {dealers.map((dealer) =>
              dealer.id ? (
                <tr key={dealer.id}>
                  <td>
                    <Link to={`/dealer/${dealer.id}`}>{dealer.full_name}</Link>
                  </td>
                  <td>{dealer.city}</td>
                  <td>{dealer.st}</td>
                  <td>
                    <Link to={`/postreview/${dealer.id}`}>Post Review</Link>
                  </td>
                </tr>
              ) : null
            )}
          </tbody>
        </table>
      ) : (
        <p>No dealers found.</p>
      )}
    </div>
  );
}

export default Dealers;