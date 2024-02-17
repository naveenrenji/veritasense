import "./Home.css";
import Container from "react-bootstrap/Container";

function Home() {
  return (
    <Container>
      <div className="intro-div">
        <h3>
        Welcome to Veritasense! 

        </h3>
        <div>
          <br></br>

          <p className="intro-text">
          Step into a space where conversations are powered by the expertise of Professor Carlo Lipizzi.
         Our chatbot is fine-tuned on specialized topics, offering you precise and insightful responses.
          Engage with a blend of cutting-edge technology and academic wisdom, tailored to enrich your interaction.
           Veritasense is here to make every conversation count. Let's begin this journey of discovery together!

          </p>
          <p>
          </p>
        </div>
      </div>
    </Container>
  );
}

export default Home;
