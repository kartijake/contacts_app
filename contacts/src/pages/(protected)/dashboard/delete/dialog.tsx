import { Button } from "@/components/ui/button"
import {
  Dialog,
  DialogClose,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger
} from "@/components/ui/dialog"
import { toast } from "@/hooks/use-toast"
import useContactStore from "@/states/useContactStore"
import { Dispatch } from "react"

export function DeleteDialog({
  deleteId,
  clearDeleteId
}: {
  deleteId: number
  clearDeleteId: Dispatch<React.SetStateAction<null>>
}) {
  const { deleteContact } = useContactStore()
  const handleDelete = async () => {
    await deleteContact(deleteId)
    if (useContactStore.getState().error) {
      toast({
        title: "Error deleting contact",
        description: useContactStore.getState().error,
        variant: "destructive"
      })
    } else {
      toast({
        title: "Done",
        description: "Contact removed"
      })
      clearDeleteId(null)
      document.getElementById("closeDeleteDialogButton")?.click()
    }
  }
  return (
    <Dialog>
      <DialogTrigger asChild>
        <Button id='deleteContactOpenButton' className='sr-only' variant='outline'>
          Delete Contact
        </Button>
      </DialogTrigger>
      <DialogContent className='sm:max-w-[425px]'>
        <DialogHeader>
          <DialogTitle>Are you sure?</DialogTitle>
          <DialogDescription>This action cannot be undone, are you sure you want to delete this.</DialogDescription>
        </DialogHeader>

        <DialogFooter>
          <Button onClick={handleDelete}>Yes</Button>
          <DialogClose asChild>
            <Button id='closeDeleteDialogButton' variant={"outline"}>
              No
            </Button>
          </DialogClose>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  )
}
