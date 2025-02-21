import { FormLayout } from "../layout"
import AuthForm from "../form"

export default function SignUp() {
  return (
    <FormLayout title='Sign Up' description='create an account'>
      <AuthForm isSignUp={true} />
    </FormLayout>
  )
}
