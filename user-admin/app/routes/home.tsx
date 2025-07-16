import type { Route } from "./+types/home";
import { Form, useLoaderData } from "react-router";
import UsersList from "~/components/UsersList";

export const action = async ({ request }: Route.ActionArgs) => {
  const formData = await request.formData();
  const name = formData.get("name");
  const email = formData.get("email");

  const response = await fetch("http://localhost:8080/users", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ name, email }),
  });

  if (!response.ok) {
    throw new Error("Failed to create user");
  }

  return null;
};

export const loader = async ({ request }: Route.LoaderArgs) => {
  const response = await fetch("http://localhost:8080/users", {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
  });
  const users = await response.json();
  console.log("Users fetched:", users);
  return { users };
};

export function meta({}: Route.MetaArgs) {
  return [
    { title: "New React Router App" },
    { name: "description", content: "Welcome to React Router!" },
  ];
}

export default function Home() {
  const { users } = useLoaderData<typeof loader>();
  return (
    <>
      <UsersList users={users} />
      <Form method="post">
        <input type="text" name="name" placeholder="Name" />
        <input type="email" name="email" placeholder="Email" />
        <button type="submit">Create User</button>
      </Form>
    </>
  );
  // return <Welcome />;
}
