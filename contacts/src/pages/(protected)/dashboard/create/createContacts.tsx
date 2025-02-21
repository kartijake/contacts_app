import { Drawer, DrawerClose, DrawerContent, DrawerHeader, DrawerTitle, DrawerTrigger } from "@/components/ui/drawer"
import { PlusIcon } from "lucide-react"
import ContactForm, { UpdateContactFormData } from "./form"
import { Button } from "@/components/ui/button"
import { Dispatch } from "react"

export default function CreateContacts({
  updateData,
  clearUpdate
}: {
  updateData?: Partial<UpdateContactFormData>
  clearUpdate: Dispatch<React.SetStateAction<null>>
}) {
  return (
    <Drawer>
      <DrawerTrigger asChild>
        <Button id='contactFromDrawerButton'>
          <PlusIcon />
          {updateData ? "Update contact" : "Add contact"}
        </Button>
      </DrawerTrigger>
      <DrawerContent>
        <div className='max-w-xl mx-auto w-full'>
          <DrawerHeader className='overflow-auto max-h-[500px]'>
            <DrawerTitle>{updateData ? "Update current contact" : "Create a new contact"}</DrawerTitle>
            <ContactForm updateData={updateData} clearUpdate={clearUpdate} CancelDrawer={CloseDraw} />
          </DrawerHeader>
        </div>
      </DrawerContent>
    </Drawer>
  )
}
const CloseDraw = () => {
  return (
    <DrawerClose asChild id='drawerClose'>
      <Button variant={"outline"}>Cancel</Button>
    </DrawerClose>
  )
}
