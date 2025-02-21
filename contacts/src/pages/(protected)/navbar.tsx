import useAuthStore from "@/states/useAuthStore"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger
} from "@/components/ui/dropdown-menu"
import { LogOut, Mail, Signature } from "lucide-react"
import { Link } from "react-router-dom"

const Navbar: React.FC = () => {
  const { user } = useAuthStore()

  return (
    <nav className=' sticky top-0 z-50 w-full border-b border-gray-50 bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60'>
      <div className='max-w-[1400px] border-x border-dashed px-6 mx-auto flex justify-between py-3'>
        <Link className='mr-4 flex items-center gap-2 lg:mr-6' to='/dashboard'>
          <Signature />
          <span className='hidden font-bold lg:inline-block'>My/Contacts</span>
        </Link>

        <div className='flex items-center space-x-4 cursor-pointer'>
          {user.isAuthenticated && (
            <>
              <DropdownMenuDemo>
                <Avatar>
                  <AvatarImage src='https://avatar.iran.liara.run/public' />
                  <AvatarFallback>{user.email.slice(0, 2).toUpperCase()}</AvatarFallback>
                </Avatar>
              </DropdownMenuDemo>
            </>
          )}
        </div>
      </div>
    </nav>
  )
}

export default Navbar

export function DropdownMenuDemo({ children }: { children: React.ReactNode }) {
  const { user, logout } = useAuthStore()

  return (
    <DropdownMenu>
      <DropdownMenuTrigger asChild>{children}</DropdownMenuTrigger>
      <DropdownMenuContent className='w-56'>
        <DropdownMenuLabel>My Account</DropdownMenuLabel>
        <DropdownMenuSeparator />

        <DropdownMenuItem disabled>
          <Mail />
          {user.email}
        </DropdownMenuItem>
        <DropdownMenuItem onClick={logout}>
          <LogOut />
          Log out
        </DropdownMenuItem>
      </DropdownMenuContent>
    </DropdownMenu>
  )
}
