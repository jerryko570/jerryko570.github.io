---
layout: post
title: "TextInput 리팩토링: 책임 분리와 Compound 패턴"
description: "TextInput 복잡성 문제를 cva·Compound 패턴·forwardRef로 해결한 Field 단위 리팩토링"
date: 2025-12-22 00:00:00 +0900
categories: [frontend]
tags: [react, typescript, cva, component, design-system, compound-pattern]
image: /assets/img/thumbnail/self-study.png
---

> **Self Study · Component Architecture**
TextInput 컴포넌트는 처음에는 가장 단순한 입력 컴포넌트처럼 보였다. 하지만 프로젝트 규모가 커지면서 TextInput 하나에 너무 많은 책임이 쌓이기 시작했고, 이 글은 그 문제를 **컴포넌트 리팩토링 관점에서 어떻게 해결했는지**를 정리한 기록이다.

---

## **1️⃣ 작업했던 TextInput이 복잡해진 이유**

TextInput은 초반에는 `placeholder` 하나만 있어도 충분했다. 필요한 옵션이 생길 때마다 `props`를 하나씩 추가하는 방식으로 빠르게 구현할 수 있었고, 그 자체로는 큰 문제가 없어 보였다.

문제는 프로젝트가 커지기 시작하면서부터였다. 아이콘, 버튼, 에러 메시지, 상태 값들이 계속 붙었고, 어느 순간 TextInput은 **입력과 관련된 거의 모든 역할을 혼자서 맡고 있는 컴포넌트**가 되어 있었다.


```tsx
// TextInput props
export default function TextInput({
label,
size,
status = "default",
icon = true,
button = true,
placeholder,
value,
clearable,
errorMessage,
onChange,
aria,
}: TextInputProps)
```


처음에는 옵션이 많아졌네 정도로만 느껴졌지만, 심화 프로젝트를 진행하면서 생각이 조금 달라졌다. 기능을 더 잘 만드는 것 보다 이 컴포넌트가 어디까지 책임지는게 맞는지를 먼저 고민해야겠다는 생각이 들었고, 이 질문에서 스터디가 시작되었다.

> 💡 **TextInput은 어디까지 책임지는 게 맞을까?**

---


## **2️⃣ TextInput 스타일 책임 분리: cva 도입**

TextInput이 복잡해진 이유를 하나씩 뜯어보니, 가장 먼저 눈에 띈 건 스타일이었다. `size, status, disabled` 같은 UI 상태들이 조건문 형태로 컴포넌트 내부에 흩어져 있었고, 스타일 규칙이 늘어날수록 코드도 함께 무거워지고 있었다.

그래서 가장 먼저 한 선택은 스타일 책임을 컴포넌트 밖으로 꺼내는 것이었다.

---

### **👉🏻 cva로 스타일 규칙 분리**
`cva`를 도입하면서 TextInput 내부에서 상태에 따라 클래스를 직접 계산하지 않게 되었다.
대신 **이 상태면 이 스타일**이라는 규칙을 variant로 정리해 한 곳에 모아놓았다.

```ts
// TextInput의 스타일 규칙을 정의하는 cva 설정
// 컴포넌트 내부에서 조건문으로 스타일을 계산하지 않기 위해 분리
export const textInputStyle = cva(
  ['inline-flex items-center w-full', 
  'rounded-lg border px-4'],
  {
    variants: {
      size: {
        sm: 'h-9 text-sm',
        md: 'h-13.5 text-base',
      },
      state: {
        default: 'border-gray-200 hover:border-gray-500',
        error: 'border-red-500',
      },
    },
    defaultVariants: {
      size: 'md',
      state: 'default',
    },
  }
);
```

이 과정을 거치며 TextInput은 스타일을 계산하는 역할에서 벗어나, 상태에 따라 스타일을 선택하는 컴포넌트로 바뀌었다.
다만 스타일만 정리됐을 뿐이고 구조에 대한 고민은 아직 해결되지 않은 상태...😳

---

## **3️⃣ Input이 아닌 Field 단위로 컴포넌트 바라보기**
`cva`로 스타일은 정리했지만, 여전히 하나의 컴포넌트가 `label` `input` `message`까지 모두 책임지고 있었다.
스타일만 분리됐을 뿐, TextInput이 맡고 있는 역할의 범위는 크게 달라지지 않은 상태였다.

여러 사례를 찾아보면서 Input을 하나의 요소로 보는 것보다, **입력 필드(Field)**라는 단위로 바라보는 편이 더 자연스러웠다. 사용자에게 입력은 input 하나가 아니라 label과 에러 메시지가 함께 묶인 하나의 맥락(Context)이기 때문이다. 그래서 Input은 필드의 일부로 두고, label과 message를 같은 맥락 안에서 함께 다루기로 했다.

---

## **4️⃣ forwardRef와 Compound 패턴으로 역할 경계 나누기**
이 구조에서 `forwardRef`와 `Compound` 패턴을 선택한 이유는 지금 당장 꼭 필요해서라기보다는,
경계를 직접 나눠보는 연습에 가까웠다.

`forwardRef` 부모가 input에 직접 접근해서 focus 같은 행동을 제어할 수 있게 사용함 <br/>
`Compound` label, input, message를 하나의 Field 맥락으로 묶기 위함

패턴 자체를 쓰는 것이 목적이 아니라 어디까지를 하나의 컴포넌트로 볼 것인지 감을 잡는 과정이었다.

---

## **5️⃣ TextField 컴포넌트 구조 설계**
그 결과, TextInput 대신 TextField라는 구조로 나누게 되었다.
기준은 단순했다. 역할별로 나누기.

```shell
TextField/
 ├─ TextField (id, status)
 ├─ Label          
 ├─ Input (+ ref)
 └─ Message (에러 메시지)
 ```

## **6️⃣ TextField는 상황만 만든다**
TextField는 값을 직접 관리하지 않는다. `id`를 생성해 label과 input을 연결하고, 현재 상태`status, error`만 하위 컴포넌트에 전달한다. <br/>

👉🏻 값도, 이벤트도 관리하지 않는다. 
👉🏻 연결과 맥락만 책임진다.

```tsx
const TextFieldContext = createContext(null);

export function TextField({ state = 'default', children }) {
  const id = useId();

  return (
    <TextFieldContext.Provider value={{ id, state }}>
      {children}
    </TextFieldContext.Provider>
  );
}
```

## **7️⃣ Label과 Input은 각자 역할만 한다**
Label과 Input은 각각 하나의 역할만 맡도록 분리했다.
Label은 텍스트를 보여주고 input과 연결하는 역할만 하고, Input은 입력을 담당하며 필요할 경우 외부에서 `focus`를 제어할 수 있도록 `ref`를 전달받는다.

```tsx
// Label: 텍스트를 보여주고 input과 연결
// label을 클릭하면 연결된 input에 자동으로 포커스됨
export function TextFieldLabel({ children }) {
  const { id } = useContext(TextFieldContext);
  return <label htmlFor={id}>{children}</label>;
}
```

```tsx
// Input: 실제 입력을 담당
// ref를 통해 외부에서 포커스 같은 행동을 제어할 수 있음
export const TextFieldInput = forwardRef((props, ref) => {
  const { id, state } = useContext(TextFieldContext);

  return (
    <input
      id={id}
      ref={ref}
      aria-invalid={state === 'error'}
      {...props}
    />
  );
});
```

## **8️⃣ 사용하는 쪽에서 드러나는 구조**
사용하는 쪽에서는 구조가 자연스럽게 드러난다. 접근성은 자동으로 챙겨지고, 필요하면 focus 같은 행동도 제어할 수 있다.

```tsx
<TextField state="error">
  <Label>Email</Label>
  <Input ref={inputRef} />
  <Message>이메일을 입력해주세요</Message>
</TextField>
```

## **9️⃣ 결론: 컴포넌트보다 중요한 건 책임의 경계**
이번 설계의 목적은 TextInput을 잘게 쪼개는 데 있지 않았다. Input과 Field의 경계를 어디에 둘지 직접 판단해보는 과정이었다.

`cva`는 스타일 책임을 분리해줬고, Compound 패턴은 구조와 의미를 묶어줬으며,
`forwardRef`는 input의 행동을 외부에서 제어할 수 있게 해주었다.

결국 이 작업은 컴포넌트를 잘 만드는 연습이라기보다, **무엇을 어디까지 책임지게 할지 선택하는 연습**에 가까웠다.
TextInput을 분리하면서 컴포넌트 자체보다 책임의 경계를 결정하는 감각이 더 중요하다는 점을 배웠다.

---

## **⭐️ 마지막으로, UX 디자인 관점에서 이 작업을 통해 배운 점**
이번 작업을 통해 UX에서 중요한 것은 개별 요소가 아니라 **같은 맥락(Context)을 공유하는 구조**라는 점을 다시 확인했다.

각 요소가 자기 역할에만 집중하도록 구조화하면 label, input, 상태, 피드백이 하나의 맥락 안에서 자연스럽게 연결되고,
그 결과 구현 방식에 따라 UX가 달라질 가능성은 줄어들고 사용자 경험은 더 안정적이고 일관되게 유지될 수 있다는 결론을 내리게 되었다.
