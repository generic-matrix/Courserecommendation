import Container from 'react-bootstrap/Container';
import './App.css';
import ReactSearchBox from "react-search-box";
import 'bootstrap/dist/css/bootstrap.min.css';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Button from 'react-bootstrap/Button';
import Card from 'react-bootstrap/Card';
import React,{useState} from 'react';
import service from './Recommendation';
import Recommendation from './Recommendation';

function App() {

  const [title, setTitle] = useState("");
  const [data, setData] = useState([]);
  const [recommendations,SetRecommendations]=useState(undefined);
  return (
    <div>
      <div className="App">
        <header className="App-header">
          <h1 style={{color:"white"}}>Recommend me the courses</h1>
          <Row className="justify-content-md-center">
            <ReactSearchBox
              placeholder="Search For The courses Here"
              value={title}
              data={data}
              inputFontColor="white"
              inputFontSize="40"
              inputBackgroundColor="#282c34"
              onChange={(text)=>{
                setTitle(text)
                service.Autocomplete(text).then((d)=>{
                  setData(d)
                }).catch((error)=>{
                  console.log(error)
                })
              }}
              onSelect={(obj)=>{
                const text = obj.item.value;
                service.Recommendation(text).then((d)=>{
                  if(d!==undefined){
                    if(d.error===null){
                      var arr = []
                      Object.keys(d.data).forEach(function(key) {
                        var value = d.data[key];
                        arr.push(value);
                      });
                      SetRecommendations(arr)
                    }else{
                      SetRecommendations(d.error)
                    }
                  }
                }).catch((error)=>{
                  console.log(error)
                })
              }}
            />
          </Row>
          <div style={{height:20}}></div>
          <Container fluid>
            <Col>
            {
              (recommendations!==undefined)?
                (typeof(recommendations)==="object")?
                  recommendations.map((recommendation)=>{
                    return <Card bg={'dark'} className="mb-2" style={{ width:'100%',paddingRight:20 }} text={'white'} border="light">
                      <Card.Body>
                        <Card.Text>{recommendation.course_title}</Card.Text>
                        <Button variant="primary" onClick={()=>{ window.open(recommendation.url)}} >Learn More</Button>
                      </Card.Body>
                    </Card> 
                  }):<h1 style={{color:"white"}}>{recommendations}</h1>
                :<></>
            }  
            </Col>
        </Container>
        </header>
      </div>
    </div>
  );
}

export default App;
