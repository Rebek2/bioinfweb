import React,{Component} from 'react';


//Collecting data from API

class Blog extends Component{

    constructor(props){
        super(props);
        this.state = {
            items:[],
            isLoaded: false,
    }
}
componentDidMount(){
    fetch('http://127.0.0.1:8000/api/posts/')
    .then(res=>res.json())
    .then(json=>{
        this.setState({
            isLoaded:true,
            items:json,
        })
    })
}

render()
{
    var {isLoaded,items} = this.state;
    if(!isLoaded){
        return <div>Ładuję . . .</div>
    }
    else{
        return(
            <div>
            
                
                    {items.map(item=>(
                        
                        <div class = 'card'  key={item.id}>
                            
                         <div class = 'card-header'>Tytuł: {item.title} | Autor: {item.author} | {item.date_created}</div>
                           <div class ='card-body'>{item.content} </div>
                           

                                 
                           
                           
                        </div>
                        
                    ))}
                
            </div>
        
        )
    }
}
}


function App2() {
    return(
      <div class = 'container'>
          <h2>Wszystkie posty:</h2>
        <Blog/>
      </div>
    )
  }
  
export default App2;