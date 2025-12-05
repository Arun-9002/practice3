import React, { useState } from "react";

export default function FormPractice() {

  const [email, setEmail] = useState("");
  const [phone, setPhone] = useState("");
  const [error, setError] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    setError("");

    // --- VALIDATIONS ---

    if (!email) {
      setError("Email is required");
      return;
    }

    // simple email pattern check
    if (!email.includes("@")) {
      setError("Invalid email format");
      return;
    }

    if (!phone) {
      setError("Phone number is required");
      return;
    }

    if (phone.length !== 10) {
      setError("Phone number must be 10 digits");
      return;
    }

    alert("Form submitted successfully!");
  };

  return (
    <div>
      <h2>Task 3 — Forms + Validation</h2>

      {error && <p style={{ color: "red" }}>{error}</p>}

      <form onSubmit={handleSubmit}>

        <input 
          placeholder="Enter email"
          value={email}
          onChange={(e)=>setEmail(e.target.value)}
        /><br /><br />

        <input 
          placeholder="Enter phone"
          value={phone}
          onChange={(e)=>setPhone(e.target.value)}
        /><br /><br />

        <button type="submit">Submit</button>
      </form>
    </div>
  );
}
