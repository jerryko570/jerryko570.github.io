---
layout: post
title: "React에서 API 데이터 불러오기 | useEffect 실전 패턴"
description: "useEffect를 사용해 API 데이터를 불러오며 상태 변화와 렌더링이 어떻게 연결되는지 실제 프로젝트 경험을 기준으로 정리했습니다."
date: 2025-09-05 00:00:00 +0900
categories: [frontend, react, javascript]
tags:
  - react
  - api
  - async
  - useEffect
  - fetch
  - axios
  - rendering
series: toyproject
image: /assets/img/thumbnail/toy-project.png
---

## **⭐️목표⭐️**
- ### **React에서 실제 API 데이터를 불러오기**
> `fetch()`와 `async/await`를 활용해 상품 리스트 렌더링하기 <br />
> `axios`는 다음 미니 프로젝트 때 반영할 예정
> `useEffect`로 로딩과 에러 상태를 함께 관리하기  

---

- ### **핵심포인트**
- API 함수 만들기 (`getProductsApi`)
- `useEffect()`로 데이터 호출
- `map()`으로 리스트 렌더링
- 로딩 및 에러 UI 분기 처리

---

- ### **결과 미리보기**

<div style="display: flex; justify-content: center; gap: 20px; align-items: center; flex-wrap: wrap;">

  <div style="text-align: center;">
    <img src="/assets/img/self-study/mini-project-api-web.gif"
         alt="API 호출 후 웹 상태"
         width="600"
         style="border-radius: 12px;" />
  </div>

  <div style="text-align: center;">
    <img src="/assets/img/self-study/mini-project-api-mobile.gif"
         alt="API 호출 후 모바일 상태"
         width="400"
         style="border-radius: 12px; " />
  </div>

</div>


---

## **1. 프로젝트 구조**
```bash
src/
├── api/ #FakeStore API에서 상품 데이터 요청
│   └── getProductsApi.js             
│
├── products/ # 상품 관련 기능 전용 폴더 
│   ├── components/                     
│   │   ├── ProductCard.jsx # 개별 상품 카드 UI
│   │
│   ├── hooks/ # 상품 데이터 관련 훅
│   │   └── useProductsList.js 
│   │
│   └── pages/ # 상품 관련 페이지 (데이터 map() 랜더링)
│       └── ProductListsPage.jsx         
│
└── App.jsx # 앱 전체 엔트리 포인트
```

## **2. API 함수 만들기 - getProductsApi**
- `fetch (async await)`로 데이터 요청
- 서버로 상품 데이터를 요청하고 json 형태로 응답받음

```js
// src/api/getProductsApi.js
export async function getProductsApi() {
   try { 
      // 1.서버 요청 (Request)
      const res = await fetch
      ("https://fakestoreapi.com/products") 
      // 더미 데이터 ➡ Promise 처리까지 기다림

      // 2.응답 검사 (200~299 외엔 오류 처리)
      if(!res.ok) {
         throw new Error 
         ("상품 데이터를 불러오지 못했습니다.", (`${res.status}`))
      }

      // 3.json 변환 (문자열에서 JS객체로) ➡️ ✔️훅에 변환된 데이터 전달
      const data = await res.json(); 
      return data; 
   }

   // 4.오류 결과 반환
   catch (err) {
      console.err("ProductsApi err", err); 
      return null // 앱이 멈추지 않게 빈값 반환
   }
}
```

## **3. 커스텀 훅 만들기 - useProductList**

```jsx
// src/components/ProductListHook.js
import { useState, useEffect } from "react";
import { ProductsApi } from "../api/getProductsApi";

// 상품 리스트를 불러오는 커스텀 훅
export default function ProductListHook() {
  const [products, setProducts] = useState([]); 
  const [loading, setLoading] = useState(true); 
  const [error, setError] = useState(null);     

  useEffect(() => {
    // 비동기 데이터 요청 함수
    async function fetchData() {
      try {
        const data = await getProductsApi();              
        setProducts(data || []); // ➡️ ✔️전달받은 데이터 상태로 저장                
      } catch (err) {
        setError(err.message || "데이터를 불러오지 못했습니다."); 
      } finally {
        setLoading(false);                             
      }
    }

    fetchData(); // 컴포넌트 마운트 시 실행
  }, []);

  // 상태 반환 (컴포넌트에서 사용)
  return { products, loading, error }; 
}
```

## **4. 상품 리스트 UI - ProductListPage**
- `map()` 메서드를 사용하여 API에서 받아온 상품 배열을 순회해
**각 상품 정보를 ProductCard 컴포넌트로 렌더링**한다.

```jsx
// src/products/pages/ProductListPage.jsx
import { useProductList } from "../hooks/useProductList";
import ProductCard from "./ProductCard";

// 상품 리스트 페이지 
export default function ProductListPage() {

  // 커스텀 훅에서 상태 가져오기 ➡️ ✔️products는 이미 서버에서 받아온 상품 배열
  const { products, loading, error } = useProductList();

  if (loading) return <p className="text-center mt-10">⏳ 로딩 중...</p>;
  if (error) return <p className="text-center text-red-600">{error}</p>;

  // 상품 리스트 렌더링 (반응형 grid 구성) ➡️ ✔️map(): 상품을 화면에 출력
  return (
    <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-8">
      {products.map((item) => (
        <ProductCard // ➡️ ✔️ProductCard에 상품 데이터 props로 전달 
          key={item.id}
          title={item.title}
          price={item.price}
          image={item.image}
          category={item.category}
        />
      ))}
    </div>
  );
}
```
ㅔ
## **5. 단일 상품 카드 UI - ProductCard**

```jsx
// src/products/components/ProductCard.jsx
export default function ProductCard({ title, price, image, category }) {

  // 카테고리 뱃지 스타일 정의
  const badgeStyle = {
    "men's clothing": "bg-blue-600 text-white",
    "women's clothing": "bg-pink-500 text-white",
    electronics: "bg-green-600 text-white",
    jewelery: "bg-yellow-400 text-black",
  };

  const style = badgeStyle[category] || "bg-gray-500 text-white";

  // 카드 UI 디자인 정의
  return (
    <div className="flex flex-col items-center max-w-[250px]">
      <img
        src={image}
        alt={title}
        className="w-[250px] h-[250px] object-cover rounded-[24px] border border-gray-200 mt-6"
      />
      <h1 className="text-lg font-semibold mt-4 text-center line-clamp-2 overflow-hidden">{title}</h1>
      <p className="text-gray-700 text-md mt-1">{price} 달러</p>
      <div className={`mt-3 px-3 py-1 rounded-md text-sm font-semibold ${style}`}>
        {category}
      </div>
    </div>
  );
}
```

## **6. 결과 확인하기**
> 👉 <a href="https://inquisitive-pika-977d0f.netlify.app/" target="_blank" rel="noopener noreferrer">
> <strong>미니 프로젝트 바로가기</strong>
> </a>  
> 👉 <a href="https://fakestoreapi.com/products" target="_blank" rel="noopener noreferrer">
> <strong>FakeStore API JSON 참고</strong>
> </a>   

---

## 7. **마무리 하면서 느낀 점**
- 이번 미니 프로젝트를 하면서 단순히 API를 불러오는 것 보다
**데이터 흐름을 이해하고, 컴포넌트 단위로 구조화 하는 과정**을 이해할 수 있었다. 특히, 어려웠던 부분을 정리해보자면..

#### **비동기 흐름 이해**
- `fetch()` 는 바로 데이터를 반환하지 않고 `Promise`를 반환하기 때문에 `await`로 기다린 뒤 값을 받아야 한다는 점이 헷갈렸다.
> 데이터는 `getProductsApi` ➡  `useProducstList` ➡  `ProductListPage` ➡ `ProductCard`로 흘러간다. (각 단계는 서로 “props”와 “state”를 통해 연결됨)

#### **로딩/에러 상태 분리**
- 데이터가 없을 때 화면이 비어 보이는 문제를 해결하려면
`loading`과 `error` 상태를 따로 관리해야 했다.
- 이때 `finally` 구문을 써서 **무조건 로딩이 끝남**을 표시하는 패턴을 학습했다.

#### **컴포넌트 분리의 중요성**
- 처음에는 `fetch`코드와 `UI` 코드가 한 파일에 뒤섞여 있었는데,
`useProductList()` 커스텀 훅으로 분리하고 나니 재사용성도 높고 코드도 한눈에 보기 좋아졌다. 
- 데이터 로직은 `hooks`, 화면 로직은 `components` 라는 구조의 중요성을 체감했다.