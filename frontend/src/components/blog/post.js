import React from 'react';
import {useState,useEffect} from 'react';
import { useParams } from "react-router-dom";


function Post()
{
    const {id} = useParams();
    const [post, setPost] = useState({});
    

    useEffect(() => {
            fetch(`http://127.0.0.1:8000/api/posts/${id}`)
            .then(response=>{
                if(response.ok){
                   return response.json(); 
                }
                
                throw response;
            })

            .then(post =>{
                setPost(post);
            })
                
        })
			
    return(
    <div> 
    <h2>  {post.title}  </h2>    
    
    </div>

        )


}


export default Post;