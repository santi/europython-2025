import React, { useState, useEffect } from "react";
import {
  Calendar,
  Mail,
  Search,
  Users,
  ChevronRight,
  Plus,
  X,
  UserPlus,
} from "lucide-react";
import { Form } from "react-router";

export type User = {
  id: number;
  name: string;
  email: string;
  created_at: string;
};
const UsersList = ({ users }: { users: User[] }) => {
  const [showForm, setShowForm] = useState(false);
  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString("en-US", {
      year: "numeric",
      month: "short",
      day: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    });
  };

  const getInitials = (name: string) => {
    return name
      .split(" ")
      .map((word) => word.charAt(0))
      .join("")
      .toUpperCase();
  };

  const getAvatarColor = (id: number) => {
    const colors = [
      "bg-blue-500",
      "bg-green-500",
      "bg-purple-500",
      "bg-pink-500",
      "bg-indigo-500",
      "bg-yellow-500",
      "bg-red-500",
      "bg-teal-500",
    ];
    return colors[id % colors.length];
  };

  return (
    <div className="flex flex-row w-screen justify-center min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 p-8">
      <div className="max-w-4xl grow">
        <div className="bg-white rounded-2xl shadow-xl overflow-hidden">
          {/* Header */}
          <div className="bg-gradient-to-r from-blue-600 to-purple-600 px-8 py-6">
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-3">
                <div className="p-2 bg-white/20 rounded-lg">
                  <Users className="h-6 w-6 text-white" />
                </div>
                <div>
                  <h1 className="text-2xl font-bold text-white">Users</h1>
                  <p className="text-blue-100">Manage your user community</p>
                </div>
              </div>
              <div className="text-right">
                <div className="text-2xl font-bold text-white">
                  {users.length}
                </div>
                <div className="text-blue-100 text-sm">Total Users</div>
              </div>
              <button
                onClick={() => setShowForm(true)}
                className="cursor-pointer ml-4 px-4 py-2 bg-white/20 hover:bg-white/30 text-white rounded-lg transition-all duration-200 flex items-center space-x-2 backdrop-blur-sm"
              >
                <Plus className="h-4 w-4" />
                <span>Add User</span>
              </button>
            </div>
          </div>

          {showForm && (
            <div className="p-6 bg-slate-50 border-b border-slate-200">
              <div className="bg-white rounded-xl p-6 shadow-sm">
                <div className="flex items-center justify-between mb-6">
                  <div className="flex items-center space-x-3">
                    <div className="p-2 bg-blue-100 rounded-lg">
                      <UserPlus className="h-5 w-5 text-blue-600" />
                    </div>
                    <div>
                      <h3 className="text-lg font-semibold text-slate-800">
                        Add New User
                      </h3>
                      <p className="text-slate-500 text-sm">
                        Fill in the details below to create a new user
                      </p>
                    </div>
                  </div>
                  <button
                    onClick={() => setShowForm(false)}
                    className="p-2 text-slate-400 hover:text-slate-600 hover:bg-slate-100 rounded-lg transition-colors"
                  >
                    <X className="h-5 w-5" />
                  </button>
                </div>

                <Form method="post" className="space-y-4">
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                      <label className="block text-sm font-medium text-slate-700 mb-2">
                        Full Name *
                      </label>
                      <input
                        type="text"
                        name="name"
                        className="w-full text-black px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 transition-all duration-200 border-slate-200 focus:border-blue-500"
                        placeholder="Enter full name"
                      />
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-slate-700 mb-2">
                        Email Address *
                      </label>
                      <input
                        type="email"
                        name="email"
                        className="w-full !!bg-white text-black px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 transition-all duration-200 border-slate-200 focus:border-blue-500"
                        placeholder="Enter email address"
                      />
                    </div>
                  </div>

                  <div className="flex justify-end space-x-3 pt-4">
                    <button
                      type="submit"
                      className="cursor-pointer px-6 py-2 bg-blue-600 hover:bg-blue-700 disabled:bg-blue-400 text-white rounded-lg transition-colors flex items-center space-x-2"
                    >
                      {
                        <>
                          <Plus className="h-4 w-4" />
                          <span>Add User</span>
                        </>
                      }
                    </button>
                  </div>
                </Form>
              </div>
            </div>
          )}

          {/* Users List */}
          <div className="divide-y divide-slate-100">
            {users.length > 0 ? (
              users.map((user, index) => (
                <div
                  key={user.id}
                  className="p-6 hover:bg-slate-50 transition-all duration-200 cursor-pointer group"
                  style={{
                    animationDelay: `${index * 100}ms`,
                    animation: "fadeInUp 0.5s ease-out forwards",
                  }}
                >
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-4">
                      {/* Avatar */}
                      <div
                        className={`w-12 h-12 rounded-full ${getAvatarColor(
                          user.id
                        )} flex items-center justify-center text-white font-semibold shadow-lg`}
                      >
                        {getInitials(user.name)}
                      </div>

                      {/* User Info */}
                      <div className="flex-1">
                        <h3 className="text-lg font-semibold text-slate-800 group-hover:text-blue-600 transition-colors">
                          {user.name}
                        </h3>
                        <div className="flex items-center space-x-4 mt-1">
                          <div className="flex items-center space-x-1 text-slate-500">
                            <Mail className="h-4 w-4" />
                            <span className="text-sm">{user.email}</span>
                          </div>
                          <div className="flex items-center space-x-1 text-slate-500">
                            <Calendar className="h-4 w-4" />
                            <span className="text-sm">
                              {formatDate(user.created_at)}
                            </span>
                          </div>
                        </div>
                      </div>
                    </div>

                    {/* Action Arrow */}
                    <div className="opacity-0 group-hover:opacity-100 transition-opacity">
                      <ChevronRight className="h-5 w-5 text-slate-400" />
                    </div>
                  </div>
                </div>
              ))
            ) : (
              <div className="p-12 text-center">
                <div className="w-16 h-16 mx-auto mb-4 bg-slate-100 rounded-full flex items-center justify-center">
                  <Search className="h-8 w-8 text-slate-400" />
                </div>
                <h3 className="text-lg font-medium text-slate-800 mb-2">
                  No users found
                </h3>
              </div>
            )}
          </div>
        </div>
      </div>

      <style jsx="true">{`
        @keyframes fadeInUp {
          from {
            opacity: 0;
            transform: translateY(20px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }
      `}</style>
    </div>
  );
};

export default UsersList;
