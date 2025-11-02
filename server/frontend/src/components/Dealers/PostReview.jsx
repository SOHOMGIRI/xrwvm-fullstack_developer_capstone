import React, { useState } from "react";
import { useParams } from "react-router-dom";

function PostReview() {
  const { id } = useParams();
  console.log("PostReview ID:", id);

  const [formData, setFormData] = useState({
    name: "",
    review: "",
    purchase: false,
    purchase_date: "",
    car_make: "",
    car_model: "",
    car_year: "",
  });

  if (!id || isNaN(parseInt(id))) {
    return (
      <div style={{ padding: "20px", color: "red" }}>
        Invalid dealer ID. Cannot load review form.
      </div>
    );
  }

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData({
      ...formData,
      [name]: type === "checkbox" ? checked : value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const response = await fetch("/djangoapp/post_review/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ ...formData, dealership: parseInt(id) }),
      });

      const result = await response.json();
      alert(result.message || "Review submitted successfully!");
    } catch (error) {
      console.error("Error:", error);
      alert("Failed to submit review.");
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <h2>Submit a Review</h2>
      <input
        name="name"
        placeholder="Your name"
        value={formData.name}
        onChange={handleChange}
      />
      <textarea
        name="review"
        placeholder="Your review"
        value={formData.review}
        onChange={handleChange}
      />
      <label>
        <input
          type="checkbox"
          name="purchase"
          checked={formData.purchase}
          onChange={handleChange}
        />
        Purchased?
      </label>
      <input
        name="purchase_date"
        placeholder="YYYY-MM-DD"
        value={formData.purchase_date}
        onChange={handleChange}
      />
      <input
        name="car_make"
        placeholder="Car Make"
        value={formData.car_make}
        onChange={handleChange}
      />
      <input
        name="car_model"
        placeholder="Car Model"
        value={formData.car_model}
        onChange={handleChange}
      />
      <input
        name="car_year"
        placeholder="Car Year"
        value={formData.car_year}
        onChange={handleChange}
      />
      <button type="submit">Submit Review</button>
    </form>
  );
}

export default PostReview;