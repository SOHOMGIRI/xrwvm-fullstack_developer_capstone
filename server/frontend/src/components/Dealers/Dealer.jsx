import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';

function Dealer() {
  const { id } = useParams();
  const [dealer, setDealer] = useState({});
  const [reviews, setReviews] = useState([]);
  const [error, setError] = useState("");

  useEffect(() => {
    console.log("Dealer ID from params:", id);

    if (!id || isNaN(parseInt(id))) {
      setError("Invalid dealer ID.");
      return;
    }

    const fetchDealer = async () => {
      try {
        const resDealer = await fetch(`/djangoapp/get_dealer/${id}/`);
        const dataDealer = await resDealer.json();
        console.log("Fetched dealer:", dataDealer);
        setDealer(dataDealer);

        const resReviews = await fetch(`/djangoapp/get_reviews/${id}/`);
        const dataReviews = await resReviews.json();
        console.log("Fetched reviews:", dataReviews);
        setReviews(dataReviews);
      } catch (err) {
        console.error("Error fetching dealer data:", err);
        setError("Failed to load dealer information.");
      }
    };

    fetchDealer();
  }, [id]);

  if (error) {
    return <div style={{ margin: "20px", color: "red" }}>{error}</div>;
  }

  return (
    <div style={{ margin: "20px" }}>
      <h2>{dealer.full_name || "Dealer Name Unavailable"}</h2>
      <p>{dealer.city || "City"}, {dealer.st || "State"}</p>
      <Link to={`/postreview/${id}`}>Post Review</Link>

      <h3>Reviews:</h3>
      {Array.isArray(reviews) && reviews.length > 0 ? (
        <ul>
          {reviews.map((r) =>
            r.id ? (
              <li key={r.id}>
                <b>{r.name}</b>: {r.review} ({r.sentiment})
              </li>
            ) : null
          )}
        </ul>
      ) : (
        <p>No reviews yet.</p>
      )}
    </div>
  );
}

export default Dealer;