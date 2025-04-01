import React from "react";
import "../styles/profile.css";

const Profile = () => {
  return (
    <div className="profile-container">
      <h2>User Profile</h2>
      <div className="profile-details">
        <p><strong>Name:</strong> John Doe</p>
        <p><strong>Email:</strong> johndoe@example.com</p>
      </div>
      <div className="profile-actions">
        <button>Edit Profile</button>
        <button>Change Password</button>
        <button>Sign Out</button>
      </div>
    </div>
  );
};

export default Profile;
