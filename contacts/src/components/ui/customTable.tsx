"use client"

import * as React from "react"
import {
  ColumnDef,
  ColumnFiltersState,
  SortingState,
  VisibilityState,
  flexRender,
  getCoreRowModel,
  getFilteredRowModel,
  getPaginationRowModel,
  getSortedRowModel,
  useReactTable
} from "@tanstack/react-table"
import { ArrowUpDown, ChevronDown, Edit2, MoreHorizontal, Trash2 } from "lucide-react"

import { Button } from "@/components/ui/button"
import {
  DropdownMenu,
  DropdownMenuCheckboxItem,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuTrigger
} from "@/components/ui/dropdown-menu"
import { Input } from "@/components/ui/input"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { Contact } from "@/states/useContactStore"
import useContactStore from "@/states/useContactStore"
import { Select, SelectContent, SelectGroup, SelectItem, SelectLabel, SelectTrigger, SelectValue } from "./select"
import { toast } from "@/hooks/use-toast"
import { DeleteDialog } from "@/pages/(protected)/dashboard/delete/dialog"
import { UpdateContactFormData } from "@/pages/(protected)/dashboard/create/form"
import { Badge } from "./badge"

export default function DataTable({ AddContact }: { AddContact: React.ElementType }) {
  const { contacts, fetchContacts, page, pageSize, setPage, count, setPageSize, next, previous, searchContact } =
    useContactStore()
  const [sorting, setSorting] = React.useState<SortingState>([])
  const [columnFilters, setColumnFilters] = React.useState<ColumnFiltersState>([])
  const [columnVisibility, setColumnVisibility] = React.useState<VisibilityState>({})
  const [deleteId, setDeleteId] = React.useState<number | null>(null)
  const [updateContact, setUpdateContact] = React.useState<UpdateContactFormData | null>(null)
  const [searchTerm, setSearchTerm] = React.useState("")
  const columns: ColumnDef<Contact>[] = [
    {
      id: "srOnly",
      header: () => <div className='sr-only'>SL</div>,
      enableHiding: false
    },

    {
      accessorKey: "name",
      header: ({ column }) => {
        return (
          <Button
            className='text-left p-0'
            variant='ghost'
            onClick={() => column.toggleSorting(column.getIsSorted() === "asc")}>
            Name
            <ArrowUpDown />
          </Button>
        )
      },
      cell: ({ row }) => <div className='capitalize'>{row.getValue("name")}</div>,
      enableSorting: true
    },
    {
      accessorKey: "telephones",
      header: () => {
        return <div className='text-left'>Telephone</div>
      },
      cell: ({ row }) => {
        return (
          <div className='lowercase space-x-1'>
            {
              // eslint-disable-next-line @typescript-eslint/no-explicit-any
              (row.getValue("telephones") as []).map((item: any) => {
                return <Badge variant='outline'>{item.number}</Badge>
              })
            }
          </div>
        )
      },
      enableSorting: false
    },
    {
      id: "address",
      header: () => <div className='text-left'>Address</div>,
      cell: ({ row }) => {
        const { address_line_1, address_line_2, city, postcode, country } = row.original
        const formattedAddress = [address_line_1, address_line_2, city, postcode, country]
          .filter((part) => part && part.trim() !== "")
          .join(", ")

        return <div className='text-left font-medium'>{formattedAddress || "N/A"}</div>
      }
    },
    {
      id: "actions",
      enableHiding: false,
      cell: ({ row }) => {
        return (
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button variant='ghost' className='h-8 w-8 p-0'>
                <span className='sr-only'>Open menu</span>
                <MoreHorizontal />
              </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align='end'>
              <DropdownMenuLabel>Actions</DropdownMenuLabel>
              <DropdownMenuItem
                onClick={() => {
                  setUpdateContact({
                    name: row.original.name,
                    telephones: row.original.telephones,
                    address_line_1: row.original.address_line_1 as string,
                    address_line_2: row.original.address_line_2 as string,
                    city: row.original.city as string,
                    country: row.original.country as string,
                    id: row.original.id
                  })
                  document.getElementById("contactFromDrawerButton")?.click()
                }}>
                <Edit2 /> Edit
              </DropdownMenuItem>
              <DropdownMenuItem
                onClick={() => {
                  const dialog = document.getElementById("deleteContactOpenButton")
                  if (dialog) {
                    dialog.click()
                    setDeleteId(row.original.id)
                  }
                }}
                className='hover:bg-red-600! hover:text-white!'>
                <Trash2 /> Remove
              </DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>
        )
      }
    }
  ]

  React.useEffect(() => {
    fetchContacts()
    if (useContactStore.getState().error) {
      toast({
        title: "Error getting contacts",
        description: useContactStore.getState().error,
        variant: "destructive"
      })
    }
  }, [page, pageSize])

  const table = useReactTable({
    data: contacts as Contact[],
    columns,
    onSortingChange: setSorting,
    onColumnFiltersChange: setColumnFilters,
    getCoreRowModel: getCoreRowModel(),
    getPaginationRowModel: getPaginationRowModel(),
    getSortedRowModel: getSortedRowModel(),
    getFilteredRowModel: getFilteredRowModel(),
    onColumnVisibilityChange: setColumnVisibility,
    manualPagination: true,
    state: {
      sorting,
      columnFilters,
      columnVisibility
    }
  })

  React.useEffect(() => {
    const delayDebounceFn = setTimeout(async () => {
      if (searchTerm.trim() !== "") {
        await searchContact(searchTerm)
      } else {
        await fetchContacts()
      }
    }, 500)

    return () => clearTimeout(delayDebounceFn)
  }, [searchTerm, searchContact])

  return (
    <div className='w-full'>
      <DeleteDialog
        deleteId={deleteId as number}
        clearDeleteId={setDeleteId as React.Dispatch<React.SetStateAction<null>>}
      />
      <div className='flex flex-wrap space-y-2 md:space-y-0 space-x-2 items-center py-4'>
        <Input
          placeholder='Start typing...'
          onChange={(e) => {
            setSearchTerm(e.target.value)
          }}
          className='max-w-sm'
        />
        <AddContact updateData={updateContact} clearUpdate={setUpdateContact} />
        <DropdownMenu>
          <DropdownMenuTrigger asChild>
            <Button variant='outline' className='ml-auto -mt-2 md:mt-0'>
              Columns <ChevronDown />
            </Button>
          </DropdownMenuTrigger>
          <DropdownMenuContent align='end'>
            {table
              .getAllColumns()
              .filter((column) => column.getCanHide())
              .map((column) => {
                return (
                  <DropdownMenuCheckboxItem
                    key={column.id}
                    className='capitalize'
                    checked={column.getIsVisible()}
                    onCheckedChange={(value) => column.toggleVisibility(!!value)}>
                    {column.id}
                  </DropdownMenuCheckboxItem>
                )
              })}
          </DropdownMenuContent>
        </DropdownMenu>
      </div>
      <div className='rounded-md border  overflow-x-auto'>
        <Table className='min-w-[700px]'>
          <TableHeader>
            {table.getHeaderGroups().map((headerGroup) => (
              <TableRow key={headerGroup.id}>
                {headerGroup.headers.map((header) => {
                  return (
                    <TableHead key={header.id}>
                      {header.isPlaceholder ? null : flexRender(header.column.columnDef.header, header.getContext())}
                    </TableHead>
                  )
                })}
              </TableRow>
            ))}
          </TableHeader>
          <TableBody>
            {table.getRowModel().rows?.length ? (
              table.getRowModel().rows.map((row) => (
                <TableRow key={row.id}>
                  {row.getVisibleCells().map((cell) => (
                    <TableCell key={cell.id}>{flexRender(cell.column.columnDef.cell, cell.getContext())}</TableCell>
                  ))}
                </TableRow>
              ))
            ) : (
              <TableRow>
                <TableCell colSpan={columns.length} className='h-24 text-center'>
                  No results.
                </TableCell>
              </TableRow>
            )}
          </TableBody>
        </Table>
      </div>
      <div className='grid grid-cols-1 md:flex items-center justify-end space-y-2 md:space-y-0 md:space-x-2 py-4'>
        <div className='flex-1 text-sm text-muted-foreground'>
          {table.getFilteredRowModel().rows.length} row(s) of {count}
        </div>

        <div className='md:ml-auto flex items-center gap-2'>
          <span className='text-sm md:text-base text-gray-700'>Page Size:</span>
          <Select defaultValue={pageSize.toString()} onValueChange={(e) => setPageSize(Number(e))}>
            <SelectTrigger className='w-[180px]'>
              <SelectValue placeholder='Select a fruit' />
            </SelectTrigger>
            <SelectContent>
              <SelectGroup>
                <SelectLabel>Sizes</SelectLabel>
                <SelectItem value='5'>5</SelectItem>
                <SelectItem value='10'>10</SelectItem>
                <SelectItem value='20'>20</SelectItem>
                <SelectItem value='50'>50</SelectItem>
              </SelectGroup>
            </SelectContent>
          </Select>
        </div>
        <div className='flex items-center md:justify-end space-x-2 py-4'>
          <Button variant='outline' size='sm' onClick={() => setPage(page - 1)} disabled={!previous}>
            Previous
          </Button>
          <span className='text-sm md:text-base text-gray-700'>Page: {page}</span>
          <Button variant='outline' size='sm' onClick={() => setPage(page + 1)} disabled={!next}>
            Next
          </Button>
        </div>
      </div>
    </div>
  )
}
