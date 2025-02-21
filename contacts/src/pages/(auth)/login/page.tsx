import { FormLayout } from "../layout"
import LoginForm from "../form"

export default function Login() {
  return (
    <FormLayout title='Login' description='Enter your email below to login to your account'>
      <LoginForm />
    </FormLayout>
  )
}
