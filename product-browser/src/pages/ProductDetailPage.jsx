import { useState, useEffect } from 'react';
import { useParams, Link } from "react-router";


function ProductDetailPage() {
    const { id } = useParams();
    const [product, setProduct] = useState(null);

    useEffect(() => {
        async function loadProducts() {
            const res = await fetch(`https://dummyjson.com/products/${id}`);
            const data = await res.json();

            setProduct(data);
        }

        loadProducts();
    }, [id]);

    if (!product) return <p>Loading.....</p>;

    return (
        <>
        <Link to= "/"> Back to products</Link>
            <h2>{product.title}</h2>
            <img src={product.thumbnail} alt={product.title} width="200" />
            <p>Price: ${product.price}</p>
            <p>Stock:{product.stock}</p>
            <p>Category:{product.category}</p>
            <p>Rating:{product.rating}/5</p>
            <p>Description:{product.description}</p>
            <h3>Reviews</h3>
            {product.reviews.map((review, index) => (
                <div key={index}>
                    <p>{review.reviewerName}</p>
                    <p>{review.reviewerEmail}</p>
                    <p>Rating: {review.rating}/5</p>
                    <p>{review.comment}</p>
                    <hr />
                </div>
            ))}
        </>
    );
}

export default ProductDetailPage;