import { useFieldArray, useForm } from "react-hook-form"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { Form, FormControl, FormField, FormItem, FormLabel, FormMessage } from "@/components/ui/form"
import useContactStore from "@/states/useContactStore"
import { toast } from "@/hooks/use-toast"
import { Dispatch } from "react"
import { Plus, XIcon } from "lucide-react"
import { Select, SelectContent, SelectGroup, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import countries from "@/constants/country"

interface ContactFromTypes {
  CancelDrawer?: React.ElementType
  updateData?: Partial<UpdateContactFormData>
  clearUpdate: Dispatch<React.SetStateAction<null>>
}
export interface ContactFormData {
  name: string
  address_line_1?: string
  address_line_2?: string
  city?: string
  country?: string
  postcode?: string
  telephones: { number: string }[]
}

export interface UpdateContactFormData extends ContactFormData {
  id: number
}
export default function ContactForm({ CancelDrawer, updateData, clearUpdate }: ContactFromTypes) {
  const form = useForm<ContactFormData>({
    defaultValues: {
      name: updateData?.name || "",
      address_line_1: updateData?.address_line_1 || "",
      address_line_2: updateData?.address_line_2 || "",
      city: updateData?.city || "",
      postcode: updateData?.postcode || "",
      country: updateData?.country || "",
      telephones: updateData?.telephones || [{ number: "" }]
    }
  })
  const errors = form.formState.errors
  const { addContact, updateContact } = useContactStore()

  const { fields, append, remove } = useFieldArray({
    control: form.control,
    name: "telephones"
  })

  const onSubmit = async (data: ContactFormData) => {
    if (!updateData) {
      await addContact(data)
      if (!useContactStore.getState().error) {
        toast({
          title: "Done",
          description: "Your contact has been saved!"
        })
        form.reset()
        document.getElementById("drawerClose")?.click()
      } else {
        toast({
          title: "Error adding contact",
          description: useContactStore.getState().error,
          variant: "destructive"
        })
      }
    } else {
      await updateContact({ ...data, id: updateData.id as number })
      if (!useContactStore.getState().error) {
        form.reset()
        toast({
          title: "Done",
          description: "Your contact has been updated!"
        })
        document.getElementById("drawerClose")?.click()
        clearUpdate(null)
      } else {
        toast({
          title: "Error updating contact",
          description: useContactStore.getState().error,
          variant: "destructive"
        })
      }
    }
  }
  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className='space-y-2'>
        <FormField
          control={form.control}
          name='name'
          rules={{ required: "This field is required" }}
          render={({ field }) => (
            <FormItem>
              <FormLabel>
                Name <span className='text-xs text-gray-500'>(Required)</span>
              </FormLabel>
              <FormControl>
                <Input placeholder='Give a name' {...field} />
              </FormControl>
              {errors.name && <FormMessage>{errors.name.message}</FormMessage>}
            </FormItem>
          )}
        />

        <FormLabel>
          Phone Numbers <span className='text-xs text-gray-500'>(Required)</span>
        </FormLabel>
        {fields.map((field, index) => (
          <FormField
            key={field.id}
            control={form.control}
            name={`telephones.${index}.number`}
            rules={{
              required: "This field is required",
              maxLength: { message: "Value should be at most 15 characters", value: 15 },
              minLength: { message: "Value should be at least 7 characters", value: 7 },
              validate: (value) => {
                if (!/^[\d+\-()]+$/.test(value as string)) return "This character is not allowed"
              }
            }}
            render={({ field }) => (
              <FormItem>
                <div className={`items-center flex ${fields.length > 1 ? "gap-2" : "gap-y-2"}`}>
                  <FormControl>
                    <Input type='tel' placeholder='Phone Number' {...field} value={(field.value as string) || ""} />
                  </FormControl>
                  {fields.length > 1 && (
                    <Button type='button' variant='destructive' onClick={() => remove(index)} className='text-sm px-2'>
                      <XIcon />
                    </Button>
                  )}
                </div>
                <FormMessage>{form.formState.errors.telephones?.[index]?.number?.message}</FormMessage>
              </FormItem>
            )}
          />
        ))}
        <Button type='button' variant='outline' onClick={() => append({ number: "" })} className='mt-2'>
          {<Plus />} Add Phone
        </Button>

        <FormField
          control={form.control}
          name='address_line_1'
          render={({ field }) => (
            <FormItem>
              <FormLabel>Address Line 1</FormLabel>
              <FormControl>
                <Input type='text' placeholder='Street, Building' {...field} />
              </FormControl>
            </FormItem>
          )}
        />
        <FormField
          control={form.control}
          name='address_line_2'
          render={({ field }) => (
            <FormItem>
              <FormLabel>Address Line 2 </FormLabel>
              <FormControl>
                <Input placeholder='Apartment, Suite, etc.' {...field} />
              </FormControl>
            </FormItem>
          )}
        />
        <div className='grid md:grid-cols-3 gap-3'>
          <FormField
            control={form.control}
            name='city'
            rules={{
              validate: (value) => {
                return (
                  value === "" || /^[A-Za-zÀ-ÖØ-öø-ÿ' -]+$/.test(value as string) || "This character is not allowed"
                )
              }
            }}
            render={({ field }) => (
              <FormItem>
                <FormLabel>City</FormLabel>
                <FormControl>
                  <Input placeholder='City' {...field} />
                </FormControl>
                <FormMessage>{form.formState.errors.city?.message}</FormMessage>
              </FormItem>
            )}
          />
          <FormField
            control={form.control}
            name='postcode'
            render={({ field }) => (
              <FormItem>
                <FormLabel>Postcode</FormLabel>
                <FormControl>
                  <Input placeholder='Postcode' {...field} />
                </FormControl>
                <FormMessage>{form.formState.errors.postcode?.message}</FormMessage>
              </FormItem>
            )}
          />
          <FormField
            control={form.control}
            name='country'
            render={({ field }) => (
              <FormItem>
                <FormLabel>Country</FormLabel>
                <FormControl>
                  <Select onValueChange={field.onChange} defaultValue={field.value} {...field}>
                    <SelectTrigger className=''>
                      <SelectValue placeholder='Select a country' />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectGroup>
                        {countries.map((item, key) => {
                          return (
                            <SelectItem key={`countrySelect_${key + 1}`} value={item}>
                              {item}
                            </SelectItem>
                          )
                        })}
                      </SelectGroup>
                    </SelectContent>
                  </Select>
                </FormControl>
                <FormMessage>{form.formState.errors.country?.message}</FormMessage>
              </FormItem>
            )}
          />
        </div>
        <div className='flex gap-2'>
          <Button type='submit'>Submit</Button>
          {CancelDrawer && <CancelDrawer />}
        </div>
      </form>
    </Form>
  )
}
