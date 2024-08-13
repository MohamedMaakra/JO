import React from "react";
import 'bootstrap/dist/css/bootstrap.min.css'; 
import "../styles/EventCard.css"; 


const EventCard = ({ event }) => {
  return (
    <div className="card mb-4">
      <img src={event.image} className="card-img-top event-card-img" alt={event.name} />
      <div className="card-body">
        <h5 className="card-title">{event.name}</h5>
        <p className="card-text">Date : {event.date}</p>
        <p className="card-text">Lieu : {event.location}</p>
      </div>
    </div>
  );
};

export default EventCard;
