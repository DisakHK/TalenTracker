"use client"

import { useState } from "react"
import { useRouter } from "next/navigation"
import {
  AlertCircle,
  ArrowUpDown,
  Building2,
  Calendar,
  CheckCircle2,
  ChevronRight,
  Clock,
  FileText,
  HourglassIcon,
  MapPin,
  MessageSquare,
  UserCircle,
  X,
} from "lucide-react"

import { Button } from "@/components/ui/button"
import { Card } from "@/components/ui/card"
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from "@/components/ui/dropdown-menu"
import { Badge } from "@/components/ui/badge"
import { Progress } from "@/components/ui/progress"
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from "@/components/ui/tooltip"

type ApplicationStatus = "pending" | "reviewing" | "interview" | "offer" | "rejected"

interface Application {
  id: number
  jobTitle: string
  company: string
  location: string
  appliedDate: string
  status: ApplicationStatus
  progress: number
  nextStep?: string
  lastUpdate: string
  salary: string
  type: string
  hasUnreadMessages: boolean
  timeline: {
    date: string
    status: string
    description: string
  }[]
}

const applications: Application[] = [
  {
    id: 1,
    jobTitle: "Senior Web Developer",
    company: "DWeb Solutions",
    location: "Remote",
    appliedDate: "2024-02-20",
    status: "interview",
    progress: 75,
    nextStep: "Technical Interview - March 1, 2024",
    lastUpdate: "2 hours ago",
    salary: "$120k - $150k",
    type: "Full-time",
    hasUnreadMessages: true,
    timeline: [
      {
        date: "Feb 20, 2024",
        status: "Applied",
        description: "Application submitted successfully",
      },
      {
        date: "Feb 22, 2024",
        status: "Reviewing",
        description: "Application under review by hiring team",
      },
      {
        date: "Feb 24, 2024",
        status: "Interview",
        description: "Invited for technical interview",
      },
    ],
  },
  {
    id: 2,
    jobTitle: "Frontend Developer",
    company: "Tech Innovators",
    location: "New York, NY",
    appliedDate: "2024-02-18",
    status: "reviewing",
    progress: 45,
    lastUpdate: "1 day ago",
    salary: "$90k - $110k",
    type: "Full-time",
    hasUnreadMessages: false,
    timeline: [
      {
        date: "Feb 18, 2024",
        status: "Applied",
        description: "Application submitted successfully",
      },
      {
        date: "Feb 23, 2024",
        status: "Reviewing",
        description: "Application under review by hiring team",
      },
    ],
  },
  {
    id: 3,
    jobTitle: "Full Stack Engineer",
    company: "StartUp Co",
    location: "San Francisco, CA",
    appliedDate: "2024-02-15",
    status: "offer",
    progress: 100,
    nextStep: "Review Offer Letter",
    lastUpdate: "5 hours ago",
    salary: "$130k - $160k",
    type: "Full-time",
    hasUnreadMessages: true,
    timeline: [
      {
        date: "Feb 15, 2024",
        status: "Applied",
        description: "Application submitted successfully",
      },
      {
        date: "Feb 17, 2024",
        status: "Reviewing",
        description: "Application under review by hiring team",
      },
      {
        date: "Feb 20, 2024",
        status: "Interview",
        description: "Completed technical interview",
      },
      {
        date: "Feb 24, 2024",
        status: "Offer",
        description: "Received job offer",
      },
    ],
  },
]

const statusConfig = {
  pending: {
    label: "Pending Review",
    color: "text-yellow-500",
    bgColor: "bg-yellow-500/10",
    icon: Clock,
  },
  reviewing: {
    label: "Under Review",
    color: "text-blue-500",
    bgColor: "bg-blue-500/10",
    icon: FileText,
  },
  interview: {
    label: "Interview Stage",
    color: "text-purple-500",
    bgColor: "bg-purple-500/10",
    icon: Calendar,
  },
  offer: {
    label: "Offer Received",
    color: "text-green-500",
    bgColor: "bg-green-500/10",
    icon: CheckCircle2,
  },
  rejected: {
    label: "Not Selected",
    color: "text-red-500",
    bgColor: "bg-red-500/10",
    icon: X,
  },
}

export default function ApplicationsScreen() {
  const router = useRouter()
  const [filter, setFilter] = useState<ApplicationStatus | "all">("all")

  const filteredApplications = applications.filter((app) => filter === "all" || app.status === filter)

  return (
    <TooltipProvider>
      <div className="min-h-screen w-full bg-background">
        {/* Header */}
        <header className="sticky top-0 z-50 border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
          <div className="container flex h-16 items-center justify-between">
            <div className="flex items-center space-x-4">
              <div className="flex h-10 w-10 items-center justify-center rounded-full bg-primary">
                <span className="text-lg font-bold text-primary-foreground">TT</span>
              </div>
            </div>
            <UserCircle className="h-8 w-8" />
          </div>
        </header>

        {/* Main Content */}
        <main className="container py-6">
          <div className="space-y-6">
            {/* Header Section */}
            <div className="flex items-center justify-between">
              <div className="space-y-1">
                <h1 className="text-2xl font-semibold tracking-tight">My Applications</h1>
                <p className="text-sm text-muted-foreground">Track and manage your job applications</p>
              </div>
              <DropdownMenu>
                <DropdownMenuTrigger asChild>
                  <Button variant="outline" className="space-x-2">
                    <ArrowUpDown className="h-4 w-4" />
                    <span>Sort</span>
                  </Button>
                </DropdownMenuTrigger>
                <DropdownMenuContent align="end">
                  <DropdownMenuItem>Most Recent</DropdownMenuItem>
                  <DropdownMenuItem>Status</DropdownMenuItem>
                  <DropdownMenuItem>Company Name</DropdownMenuItem>
                </DropdownMenuContent>
              </DropdownMenu>
            </div>

            {/* Status Filters */}
            <div className="flex flex-wrap gap-2">
              <Button variant={filter === "all" ? "default" : "outline"} onClick={() => setFilter("all")}>
                All Applications
              </Button>
              {Object.entries(statusConfig).map(([key, config]) => {
                const Icon = config.icon
                return (
                  <Button
                    key={key}
                    variant={filter === key ? "default" : "outline"}
                    className="space-x-2"
                    onClick={() => setFilter(key as ApplicationStatus)}
                  >
                    <Icon className="h-4 w-4" />
                    <span>{config.label}</span>
                  </Button>
                )
              })}
            </div>

            {/* Applications List */}
            <div className="space-y-4">
              {filteredApplications.map((application) => {
                const status = statusConfig[application.status]
                const StatusIcon = status.icon

                return (
                  <Card key={application.id} className="p-6 transition-shadow hover:shadow-md">
                    <div className="space-y-4">
                      {/* Header */}
                      <div className="flex items-start justify-between">
                        <div className="space-y-1">
                          <h2 className="text-xl font-semibold">{application.jobTitle}</h2>
                          <div className="flex items-center space-x-2 text-muted-foreground">
                            <Building2 className="h-4 w-4" />
                            <span>{application.company}</span>
                          </div>
                        </div>
                        <Badge className={`space-x-1 ${status.bgColor} ${status.color}`}>
                          <StatusIcon className="h-4 w-4" />
                          <span>{status.label}</span>
                        </Badge>
                      </div>

                      {/* Details */}
                      <div className="grid gap-4 sm:grid-cols-3">
                        <div className="space-y-1">
                          <div className="text-sm text-muted-foreground">Location</div>
                          <div className="flex items-center space-x-2">
                            <MapPin className="h-4 w-4" />
                            <span>{application.location}</span>
                          </div>
                        </div>
                        <div className="space-y-1">
                          <div className="text-sm text-muted-foreground">Applied On</div>
                          <div className="flex items-center space-x-2">
                            <Calendar className="h-4 w-4" />
                            <span>{application.appliedDate}</span>
                          </div>
                        </div>
                        <div className="space-y-1">
                          <div className="text-sm text-muted-foreground">Last Update</div>
                          <div className="flex items-center space-x-2">
                            <HourglassIcon className="h-4 w-4" />
                            <span>{application.lastUpdate}</span>
                          </div>
                        </div>
                      </div>

                      {/* Progress */}
                      <div className="space-y-2">
                        <div className="flex items-center justify-between text-sm">
                          <span>Application Progress</span>
                          <span>{application.progress}%</span>
                        </div>
                        <Progress value={application.progress} />
                      </div>

                      {/* Actions */}
                      <div className="flex items-center justify-between">
                        <div className="flex space-x-2">
                          <Tooltip>
                            <TooltipTrigger asChild>
                              <Button
                                variant="outline"
                                size="sm"
                                className="relative"
                                onClick={() => router.push(`/applications/${application.id}/messages`)}
                              >
                                <MessageSquare className="h-4 w-4" />
                                {application.hasUnreadMessages && (
                                  <span className="absolute -right-1 -top-1 h-2 w-2 rounded-full bg-red-500" />
                                )}
                              </Button>
                            </TooltipTrigger>
                            <TooltipContent>Messages</TooltipContent>
                          </Tooltip>
                          <Tooltip>
                            <TooltipTrigger asChild>
                              <Button
                                variant="outline"
                                size="sm"
                                onClick={() => router.push(`/applications/${application.id}/timeline`)}
                              >
                                <FileText className="h-4 w-4" />
                              </Button>
                            </TooltipTrigger>
                            <TooltipContent>View Timeline</TooltipContent>
                          </Tooltip>
                        </div>
                        <Button
                          variant="ghost"
                          className="space-x-2"
                          onClick={() => router.push(`/applications/${application.id}`)}
                        >
                          <span>View Details</span>
                          <ChevronRight className="h-4 w-4" />
                        </Button>
                      </div>

                      {/* Next Step Alert */}
                      {application.nextStep && (
                        <div className="flex items-center space-x-2 rounded-lg bg-muted p-3 text-sm">
                          <AlertCircle className="h-4 w-4 text-primary" />
                          <span>Next Step: {application.nextStep}</span>
                        </div>
                      )}
                    </div>
                  </Card>
                )
              })}
            </div>
          </div>
        </main>
      </div>
    </TooltipProvider>
  )
}

