import {useState, useEffect} from 'react'; 
import {Link} from 'react-router';
export default function ProductsPage(){
    const [products,setProducts] = useState([]);

    useEffect(()=>{
        async function loadProducts() {
            const res = await fetch("https://dummyjson.com/products")
            const data = await res.json();

            setProducts(data.products);
        }
        loadProducts();
    }, []);

    return(
        <>
        <p>Loaded {products.length} Producsts.</p>
        <ul>
            {products.map((product) =>(
                <li key= {product.id}> 
                <img src = {product.thumbnail}></img>
                {product.title}
                <h3>Price: ${product.price}</h3>
                <h3>Rating: {product.rating}</h3>
                <h3>Category: {product.category}</h3>
                <h3>{product.reviews.length} reviews</h3>
                <Link to={`/products/${product.id}`}>View Details</Link>
                </li>
            ))}
            
        </ul>
        </>
    
    );
}

