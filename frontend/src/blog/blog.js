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
            <div className='blog'> 
                <ul>
                    {items.map(item=>(
                        <li key={item.id}>
                           Tytuł: {item.title} | Autor: {item.author}
                           <div>
                               {item.content}
                           </div>
                           
                        </li>
                    ))}
                </ul>
            </div>
        )
    }
}
}
export default Blog;