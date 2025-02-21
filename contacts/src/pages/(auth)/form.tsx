import { useForm } from "react-hook-form"
import { Label } from "@/components/ui/label"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { Link } from "react-router-dom"
import useAuthStore from "@/states/useAuthStore"
import { Loader2 } from "lucide-react"

interface FormData {
  email: string
  password: string
  confirmPassword?: string
}

interface AuthFormProps {
  isSignUp?: boolean
}

export default function AuthForm({ isSignUp = false }: AuthFormProps) {
  const {
    register,
    handleSubmit,
    watch,
    formState: { errors }
  } = useForm<FormData>()
  const { login, register: authRegister, loading } = useAuthStore()

  const onSubmit = async (data: FormData) => {
    if (isSignUp) {
      await authRegister(data.email, data.password)
    } else {
      await login(data.email, data.password)
    }
  }

  // Watch password for confirm password validation
  const password = watch("password")

  return (
    <form onSubmit={handleSubmit(onSubmit)} className='flex flex-col gap-6'>
      {/* Email Field */}
      <div className='grid gap-2'>
        <Label htmlFor='email'>Email</Label>
        <Input
          id='email'
          type='email'
          placeholder='m@example.com'
          {...register("email", {
            required: "Email is required",
            ...(isSignUp
              ? {
                  pattern: {
                    value: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
                    message: "Enter a valid email address"
                  }
                }
              : {})
          })}
        />
        {errors.email && <p className='text-red-500 text-sm'>{errors.email.message}</p>}
      </div>

      {/* Password Field */}
      <div className='grid gap-2'>
        <Label htmlFor='password'>Password</Label>
        <Input
          id='password'
          type='password'
          placeholder='Enter your password'
          {...register("password", {
            required: "Password is required",
            ...(isSignUp
              ? {
                  minLength: {
                    value: 8,
                    message: "Password must be at least 8 characters long"
                  },
                  validate: (value) => {
                    if (value.length < 8) {
                      return "Password must be at least 8 characters long."
                    }
                    if (!/[A-Z]/.test(value)) {
                      return "Password must contain at least one uppercase letter."
                    }
                    if (!/[a-z]/.test(value)) {
                      return "Password must contain at least one lowercase letter."
                    }
                    if (!/\d/.test(value)) {
                      return "Password must contain at least one digit."
                    }
                    if (!/[!@#$%^&*(),.?":{}|<>]/.test(value)) {
                      return "Password must contain at least one special character."
                    }
                    return true
                  }
                }
              : {})
          })}
        />
        {errors.password && <p className='text-red-500 text-sm'>{errors.password.message}</p>}
      </div>
      {/* Confirm Password Field */}
      {isSignUp && (
        <div className='grid gap-2'>
          <Label htmlFor='confirmPassword'>Confirm Password</Label>
          <Input
            id='confirmPassword'
            type='password'
            placeholder='Confirm your password'
            {...register("confirmPassword", {
              required: "Please confirm your password",
              validate: (value) => value === password || "Passwords do not match"
            })}
          />
          {errors.confirmPassword && <p className='text-red-500 text-sm'>{errors.confirmPassword.message}</p>}
        </div>
      )}

      {/* Submit Button */}
      <Button type='submit' className='w-full'>
        {loading ? <Loader2 className='animate-spin' /> : isSignUp ? "Sign Up" : "Login"}
      </Button>

      {!isSignUp && (
        <>
          <div className='mt-4 text-center text-sm'>
            Don&apos;t have an account?{" "}
            <Link to={"/sign-up"} className='underline underline-offset-4'>
              Sign up
            </Link>
          </div>
        </>
      )}

      {isSignUp && (
        <div className='mt-4 text-center text-sm'>
          Already have an account?{" "}
          <Link to={"/"} className='underline underline-offset-4'>
            Login
          </Link>
        </div>
      )}
    </form>
  )
}
