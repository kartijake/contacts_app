import ProtectedLayout from "../layout"
import CustomTable from "@/components/ui/customTable"
import CreateContacts from "./create/createContacts"

export default function Dashboard() {
  return (
    <ProtectedLayout>
      <h2
        className='font-heading mt-12 scroll-m-20 border-b pb-2 text-2xl font-semibold tracking-tight first:mt-0'
        id='CreateContact'>
        Contacts
      </h2>
      <CustomTable AddContact={CreateContacts} />
    </ProtectedLayout>
  )
}
