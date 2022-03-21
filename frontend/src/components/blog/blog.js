import React,{Component} from 'react';
import App4 from '../navbar/navBar'
import './wyglad.css'
import { useNavigate } from "@reach/router";
//Collecting data from API
import { Link } from 'react-router-dom';

class Blog extends Component{
    

    
    constructor(props){
        super(props);
        this.state = {
            items:[],
            isLoaded:false,
     
       }
    } 
componentDidMount(){
    fetch('http://127.0.0.1:8000/api/posts/')
    .then(res=>res.json())
    .then(json=>{
        this.setState({
            items:json,
            isLoaded:true,
            })
    
        })
    .catch((error) =>{
        this.setState({
        isLoaded:false,
        })
    })

    }    


render()
{
    var {isLoaded,items} = this.state;

    if(!isLoaded){
        return (<div class = 'container'>
            
            <div>
            <center> 
                <h2>Ładuję ...</h2>
            </center>
      </div>
      <center>
        <div class="spinner-border" role="status"></div>
       </center>     
      </div>
        )
    }
    else{
        return(
            <div class = 'container'>
                
                <div class ='row align-items-center'>
                    
                    {items.map(item=>(                                               
                        <div class = 'col-6 .--4col-'>
                         <Link to={`/post/${item.id}`}>
                         <div class ='blog-diw'
                                    key={item.id}>
                         
                            
                            <div  >
                            
                                <div class ='a' >Tytuł: {item.title}| Autor: {item.author} 
                                  
                                </div>                     
                            </div>
                            
                        </div>
                        </Link>
                        </div>     
                        ))}
                        
                    </div>

                </div>
            )
        }
    }
}


function App2() {
    return(<div><App4/>
      <div class = 'container'>

        <Blog/>
      </div>
      </div>
    )
  }
  
export default App2;