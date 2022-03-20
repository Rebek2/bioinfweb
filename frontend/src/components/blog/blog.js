import React,{Component} from 'react';


//Collecting data from API

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
                         
                       
                            <div class = 'card'  key={item.id}>
                            
                                <div class = 'card-header'>Tytuł: {item.title} | Autor: {item.author} 
                                    </div>
                                    <div class ='card-body'>{item.content} 
                                        </div>                     
                            </div>
                        </div>     
                        ))}
                    </div>

                </div>
            )
        }
    }
}


function App2() {
    return(
      <div class = 'container'>
          <center>
          <h2>Wszystkie posty:</h2>
          </center>
        <Blog/>
      </div>
    )
  }
  
export default App2;